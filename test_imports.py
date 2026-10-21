
print("Testing imports...")
try:
    from langchain_core.language_models.chat_models import BaseChatModel
    print("Success: from langchain_core.language_models.chat_models import BaseChatModel")
except ImportError as e:
    print(f"FAILED: from langchain_core.language_models.chat_models import BaseChatModel -> {e}")

try:
    from langchain_core.language_models.llms import LLM
    print("Success: from langchain_core.language_models.llms import LLM")
except ImportError as e:
    print(f"FAILED: from langchain_core.language_models.llms import LLM -> {e}")

try:
    from langchain_core.embeddings import Embeddings
    print("Success: from langchain_core.embeddings import Embeddings")
except ImportError as e:
    print(f"FAILED: from langchain_core.embeddings import Embeddings -> {e}")

try:
    from langchain_core.messages import (
        BaseMessage, AIMessage, HumanMessage, SystemMessage, 
        AIMessageChunk, FunctionMessage, ToolMessage
    )
    print("Success: from langchain_core.messages import ...")
except ImportError as e:
    print(f"FAILED: from langchain_core.messages import ... -> {e}")

try:
    from langchain_core.outputs import (
        ChatGeneration, ChatGenerationChunk, ChatResult, 
        LLMResult, Generation
    )
    print("Success: from langchain_core.outputs import ...")
except ImportError as e:
    print(f"FAILED: from langchain_core.outputs import ... -> {e}")

try:
    from langchain_core.callbacks import (
        CallbackManagerForLLMRun, AsyncCallbackManagerForLLMRun
    )
    print("Success: from langchain_core.callbacks import ...")
except ImportError as e:
    print(f"FAILED: from langchain_core.callbacks import ... -> {e}")

try:
    from langchain_core.runnables import RunnableConfig
    print("Success: from langchain_core.runnables import RunnableConfig")
except ImportError as e:
    print(f"FAILED: from langchain_core.runnables import RunnableConfig -> {e}")

try:
    from langchain_core.tools import BaseTool
    print("Success: from langchain_core.tools import BaseTool")
except ImportError as e:
    print(f"FAILED: from langchain_core.tools import BaseTool -> {e}")

try:
    from langchain_core.utils.function_calling import convert_to_openai_function
    print("Success: from langchain_core.utils.function_calling import convert_to_openai_function")
except ImportError as e:
    print(f"FAILED: from langchain_core.utils.function_calling import convert_to_openai_function -> {e}")

try:
    from pydantic import Field, BaseModel, SecretStr
    print("Success: from pydantic import Field, BaseModel, SecretStr")
except ImportError as e:
    print(f"FAILED: from pydantic import Field, BaseModel, SecretStr -> {e}")
