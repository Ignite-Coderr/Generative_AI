"""
Utility Functions Module

This module contains helper functions for query analysis,
complexity detection, and intent classification.
"""

import re
from typing import List


def analyze_query_complexity(query: str) -> str:
    """
    Analyze the complexity level of a user query
    
    Args:
        query: User input query
        
    Returns:
        Complexity level: 'low', 'medium', or 'high'
    """
    query_lower = query.lower()
    
    # High complexity indicators
    high_complexity_keywords = [
        'explain', 'describe', 'architecture', 'how does', 'why does',
        'comprehensive', 'detailed', 'in-depth', 'analysis', 'research',
        'differential', 'integral', 'theorem', 'proof', 'derive',
        'framework', 'mechanism', 'implementation'
    ]
    
    # Medium complexity indicators
    medium_complexity_keywords = [
        'solve', 'calculate', 'equation', 'formula', 'algorithm',
        'algebra', 'calculus', 'matrix', 'function', 'optimize',
        'compare', 'contrast', 'evaluate'
    ]
    
    # Low complexity indicators
    low_complexity_keywords = [
        'add', 'subtract', 'multiply', 'divide', 'sum', 'total',
        'simple', 'basic', 'quick', 'what is'
    ]
    
    # Check for arithmetic patterns (very low complexity)
    if re.search(r'\d+\s*[\+\-\*/]\s*\d+', query):
        return 'low'
    
    # Count keyword matches
    high_count = sum(1 for kw in high_complexity_keywords if kw in query_lower)
    medium_count = sum(1 for kw in medium_complexity_keywords if kw in query_lower)
    low_count = sum(1 for kw in low_complexity_keywords if kw in query_lower)
    
    # Determine complexity based on matches
    if high_count > 0:
        return 'high'
    elif medium_count > 0:
        return 'medium'
    elif low_count > 0:
        return 'low'
    else:
        # Default: use query length as heuristic
        word_count = len(query.split())
        if word_count > 15:
            return 'high'
        elif word_count > 8:
            return 'medium'
        else:
            return 'low'


def determine_intent(query: str) -> str:
    """
    Determine the primary intent of a user query
    
    Args:
        query: User input query
        
    Returns:
        Intent category: 'arithmetic', 'mathematical', 'explanatory', or 'creative'
    """
    query_lower = query.lower()
    
    # Arithmetic intent
    if re.search(r'\d+\s*[\+\-\*/]\s*\d+', query):
        return 'arithmetic'
    
    # Creative/Humorous intent
    creative_keywords = [
        'roast', 'joke', 'funny', 'humor', 'creative', 'story',
        'poem', 'imagine', 'pretend', 'make me laugh'
    ]
    if any(kw in query_lower for kw in creative_keywords):
        return 'creative'
    
    # Mathematical intent (advanced)
    math_keywords = [
        'solve', 'equation', 'derivative', 'integral', 'matrix',
        'algebra', 'calculus', 'theorem', 'proof', 'differential',
        'formula', 'calculate', 'optimization'
    ]
    if any(kw in query_lower for kw in math_keywords):
        return 'mathematical'
    
    # Explanatory intent
    explanation_keywords = [
        'explain', 'what is', 'how does', 'why', 'describe',
        'tell me about', 'definition', 'meaning', 'clarify',
        'elaborate', 'detail', 'architecture', 'overview'
    ]
    if any(kw in query_lower for kw in explanation_keywords):
        return 'explanatory'
    
    # Default to explanatory if uncertain
    return 'explanatory'


def format_routing_analysis(analysis: dict) -> str:
    """
    Format routing analysis into a readable string
    
    Args:
        analysis: Dictionary containing routing analysis details
        
    Returns:
        Formatted string for display
    """
    formatted = f"""
**Routing Analysis:**

📝 **Query:** {analysis['query']}

🎯 **Detected Intent:** {analysis['detected_intent'].capitalize()}

📊 **Complexity Level:** {analysis['complexity_level'].capitalize()}

🤖 **Selected Model:** {analysis['selected_model']}

🎚️ **Similarity Score:** {analysis['similarity_score']:.4f}

⚙️ **Model Characteristics:**
   - Complexity: {analysis['model_complexity']}
   - Cost: {analysis['model_cost']}
   - Latency: {analysis['model_latency']}

💡 **Explanation:**
{analysis['explanation']}
"""
    return formatted.strip()


def extract_keywords(text: str) -> List[str]:
    """
    Extract important keywords from text
    
    Args:
        text: Input text
        
    Returns:
        List of extracted keywords
    """
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at',
        'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were'
    }
    
    # Extract words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter stop words and short words
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    
    return keywords


def calculate_confidence_level(similarity_score: float) -> str:
    """
    Convert similarity score to confidence level label
    
    Args:
        similarity_score: Numerical similarity score (0-1)
        
    Returns:
        Confidence level: 'High', 'Moderate', or 'Low'
    """
    if similarity_score > 0.7:
        return 'High'
    elif similarity_score > 0.5:
        return 'Moderate'
    else:
        return 'Low'
