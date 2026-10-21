from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any, Callable

import pandas as pd
from a2a.client.client import ClientConfig
from a2a.client.client_factory import ClientFactory
from a2a.types import Message, Task
import httpx
from src.a2a_utils import (
    create_agent_card,
    create_text_message_with_data,
    extract_text_from_message,
    get_data_part,
)
from urllib.parse import urlsplit, urlunsplit


async def _send_message(endpoint: str, message: Message) -> tuple[Message, Any]:
    # Log the endpoint we are about to connect to for easier debugging
    print(f"[orchestrator] connecting to endpoint: {endpoint!r}")
    http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(120.0, connect=30.0, read=120.0, write=120.0, pool=None)
    )
    client_config = ClientConfig(streaming=False, httpx_client=http_client)
    client = await ClientFactory.connect(endpoint, client_config=client_config)
    try:
        final_message: Message | None = None
        async for response in client.send_message(message):
            if isinstance(response, Message):
                final_message = response
            else:
                task, update = response
                if isinstance(task, Task) and task.history:
                    final_message = task.history[-1]
        if final_message is None:
            raise RuntimeError(f"Agent at {endpoint} did not return a message response.")
        card = await client.get_card()
        return final_message, card
    finally:
        await client.close()
        await http_client.aclose()


def orchestrate_sales_insights(
    csv_path: str | Path,
    *,
    output_dir: str | Path = "artifacts",
    model_overrides: dict[str, str] | None = None,
    agent_endpoints: dict[str, str] | None = None,
    progress_callback: Callable[[str, dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    """Drive agent-to-agent collaboration using remote A2A message exchanges.

    In this refactored flow, the coordinator (this function) is responsible for
    providing inputs directly to each agent. Reader still ingests the dataset,
    but Analyst and Visualizer receive data from the coordinator instead of
    strictly chaining outputs from previous agents.
    """

    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset could not be located at {path}")

    # Default endpoints for local agents (base host only; ClientFactory will fetch card at /.well-known/agent-card.json)
    endpoints = agent_endpoints or {
        "reader": "http://localhost:8001",
        "analyst": "http://localhost:8002",
        "visualizer": "http://localhost:8003",
    }

    # Use the endpoints as-is
    normalized_endpoints: dict[str, str] = dict(endpoints)

    default_models = {
        "reader": "gpt-4o-mini",
        "analyst": "gpt-4o-mini",
        "visualizer": "gpt-4o",
    }
    if model_overrides:
        default_models.update(model_overrides)

    artifacts_root = Path(output_dir)
    artifacts_root.mkdir(parents=True, exist_ok=True)

    dataset_df = pd.read_csv(path)
    dataset_csv = dataset_df.to_csv(index=False)

    async def _run() -> dict[str, Any]:
        transcript: list[dict[str, Any]] = []

        # Reader still consumes the raw dataset from the coordinator
        reader_request = create_text_message_with_data(
            "Ingest the provided sales dataset and produce a structured summary.",
            data={
                "dataset_path": str(path.resolve()),
                "csv_text": dataset_csv,
                "model": default_models["reader"],
            },
        )
        transcript.append({"from": "coordinator", "message": reader_request})
        reader_message, reader_card = await _send_message(
            normalized_endpoints["reader"], reader_request
        )
        transcript.append({"from": "LangChain Reader", "message": reader_message})
        if progress_callback:
            progress_callback("reader", {"message": reader_message})

        reader_text = extract_text_from_message(reader_message)
        reader_payload = get_data_part(reader_message) or {}

        # Analyst: coordinator provides input (can include reader results but
        # no longer relies exclusively on them). This is where you can plug in
        # whatever A2A-originated payload you want CrewAI to consume.
        analyst_input = {
            "records": reader_payload.get("records", []),
            "summary_text": reader_text,
            "metrics": reader_payload.get("metrics", {}),
            "model": default_models["analyst"],
        }

        analyst_request = create_text_message_with_data(
            "Convert the provided sales context into a decision-ready analysis.",
            data=analyst_input,
        )
        transcript.append({"from": "coordinator", "message": analyst_request})
        analyst_message, analyst_card = await _send_message(
            normalized_endpoints["analyst"], analyst_request
        )
        transcript.append({"from": "CrewAI Analyst", "message": analyst_message})
        if progress_callback:
            progress_callback("analyst", {"message": analyst_message})

        analyst_text = extract_text_from_message(analyst_message)
        analyst_payload = get_data_part(analyst_message) or {}

        # Visualizer: coordinator sends the data it wants AutoGen to use.
        visualizer_input = {
            "records": reader_payload.get("records", []),
            "analysis_text": analyst_text,
            "artifacts_dir": str((artifacts_root / "autogen").resolve()),
            "model": default_models["visualizer"],
        }

        visual_request = create_text_message_with_data(
            "Generate charts and advanced analytics for the executive summary.",
            data=visualizer_input,
        )
        transcript.append({"from": "coordinator", "message": visual_request})
        visual_message, visual_card = await _send_message(
            normalized_endpoints["visualizer"], visual_request
        )
        transcript.append({"from": "AutoGen Visualizer", "message": visual_message})
        if progress_callback:
            progress_callback("visualizer", {"message": visual_message})

        visual_text = extract_text_from_message(visual_message)
        visual_payload = get_data_part(visual_message) or {}

        cards = {
            "reader": reader_card,
            "analyst": analyst_card,
            "visualizer": visual_card,
        }

        return {
            "cards": cards,
            "transcript": transcript,
            "reader": {
                "summary": reader_text,
                "metrics": reader_payload.get("metrics"),
                "records": reader_payload.get("records"),
            },
            "analyst": {
                "analysis": analyst_text,
                "structured": analyst_payload.get("analytics_json"),
            },
            "visualizer": {
                "insights": visual_text,
                "tool_outputs": visual_payload.get("tool_outputs", []),
                "artifacts_directory": visual_payload.get("artifacts_directory"),
                "raw_messages": visual_payload.get("raw_messages", []),
            },
            "conversation_log": [
                {
                    "speaker": entry["from"],
                    "text": extract_text_from_message(entry["message"]),
                    "data": get_data_part(entry["message"]),
                }
                for entry in transcript
            ],
        }

    return asyncio.run(_run())