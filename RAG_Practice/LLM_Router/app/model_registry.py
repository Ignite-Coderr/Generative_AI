"""
Model Registry Module

This module defines available AI models with their metadata including:
- name, description, complexity, cost, and latency levels
"""

from dataclasses import dataclass
from typing import List
from enum import Enum


class ComplexityLevel(Enum):
    """Enum for model complexity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CostLevel(Enum):
    """Enum for model cost levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LatencyLevel(Enum):
    """Enum for model latency levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Model:
    """
    Data class representing an AI model and its characteristics
    
    Attributes:
        name: Model identifier
        description: Detailed description of model capabilities
        complexity: Computational complexity level
        cost: Cost level for using the model
        latency: Response time level
    """
    name: str
    description: str
    complexity: ComplexityLevel
    cost: CostLevel
    latency: LatencyLevel

    def to_dict(self):
        """Convert model to dictionary format"""
        return {
            "name": self.name,
            "description": self.description,
            "complexity": self.complexity.value,
            "cost": self.cost.value,
            "latency": self.latency.value
        }


class ModelRegistry:
    """
    Central registry for all available AI models
    
    This class maintains the list of available models and provides
    methods to access and query them.
    """
    
    def __init__(self):
        """Initialize the model registry with predefined models"""
        self.models = self._initialize_models()
    
    def _initialize_models(self) -> List[Model]:
        """
        Create and return the list of available models
        
        Returns:
            List of Model instances
        """
        return [
            Model(
                name="Small-Math",
                description="Specialized in basic arithmetic operations like addition, subtraction, multiplication, and division. Handles simple mathematical calculations quickly and efficiently. Best for elementary arithmetic problems.",
                complexity=ComplexityLevel.LOW,
                cost=CostLevel.LOW,
                latency=LatencyLevel.LOW
            ),
            Model(
                name="DeepSeek-Math",
                description="Advanced mathematical reasoning model capable of solving algebra, calculus, differential equations, and multi-step mathematical problems. Provides step-by-step solutions and mathematical proofs. Ideal for complex mathematical reasoning tasks.",
                complexity=ComplexityLevel.MEDIUM,
                cost=CostLevel.MEDIUM,
                latency=LatencyLevel.MEDIUM
            ),
            Model(
                name="Research-GPT",
                description="High-capacity model designed for in-depth explanations, research-level analysis, technical documentation, and comprehensive educational content. Excels at breaking down complex topics like machine learning architectures, scientific concepts, and theoretical frameworks.",
                complexity=ComplexityLevel.HIGH,
                cost=CostLevel.HIGH,
                latency=LatencyLevel.HIGH
            ),
            Model(
                name="Roast-GPT",
                description="Creative and humorous model specialized in witty responses, roasting, jokes, and entertaining content. Designed for casual, fun interactions with a comedic twist. Perfect for light-hearted banter and creative wordplay.",
                complexity=ComplexityLevel.LOW,
                cost=CostLevel.LOW,
                latency=LatencyLevel.LOW
            )
        ]
    
    def get_all_models(self) -> List[Model]:
        """
        Get all registered models
        
        Returns:
            List of all Model instances
        """
        return self.models
    
    def get_model_by_name(self, name: str) -> Model:
        """
        Retrieve a specific model by name
        
        Args:
            name: Model name to search for
            
        Returns:
            Model instance if found, None otherwise
        """
        for model in self.models:
            if model.name == name:
                return model
        return None
    
    def get_model_descriptions(self) -> List[str]:
        """
        Get all model descriptions for embedding generation
        
        Returns:
            List of model descriptions
        """
        return [model.description for model in self.models]
    
    def get_model_names(self) -> List[str]:
        """
        Get all model names
        
        Returns:
            List of model names
        """
        return [model.name for model in self.models]
