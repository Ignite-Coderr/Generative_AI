import requests
import json
from typing import List, Dict, Any
import re
from app.config import OPENAI_API_BASE, OPENAI_API_KEY, LLM_MODEL

TEMPERATURE = 0.7

def get_chat_model(api_key: str = None):
    """Get chat model configuration for Euron API"""
    return {
        'model': LLM_MODEL,
        'temperature': TEMPERATURE,
        'api_base': OPENAI_API_BASE,
        'api_key': OPENAI_API_KEY
    }

def ask_chat_model(chat_model, prompt: str):
    """Ask the Euron API model using direct HTTP requests"""
    try:
        # Euron API endpoint
        url = f"{OPENAI_API_BASE}/chat/completions"
        
        # Headers for Euron API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        
        # Request payload for Euron API
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": LLM_MODEL,
            "max_tokens": 1000,
            "temperature": TEMPERATURE
        }
        
        # Make the request
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            # Handle Euron API response format
            if 'choices' in data and len(data['choices']) > 0:
                choice = data['choices'][0]
                
                if 'message' in choice and 'content' in choice['message']:
                    content = choice['message']['content']
                    
                    # If content is a list (Euron format), extract text
                    if isinstance(content, list):
                        text_parts = []
                        for item in content:
                            if isinstance(item, dict) and item.get('type') == 'text':
                                text_parts.append(item.get('text', ''))
                            elif isinstance(item, str):
                                text_parts.append(item)
                        return '\n'.join(text_parts)
                    else:
                        return str(content)
                else:
                    return str(choice)
            else:
                return f"Unexpected response format: {data}"
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            print(f"Error calling Euron API: {error_msg}")
            return f"Error: Unable to get response from Euron API. {error_msg}"
            
    except requests.exceptions.Timeout:
        return "Error: Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Error: Unable to connect to Euron API. Please check your internet connection."
    except Exception as e:
        print(f"Error calling Euron API: {e}")
        return f"Error: Unable to get response from the AI model. Please check your Euron API configuration. Error: {str(e)}"

def generate_medical_insights(text: str) -> Dict[str, Any]:
    """Generate medical insights from text analysis"""
    insights = {
        'medical_terms': [],
        'potential_conditions': [],
        'medications': [],
        'vital_signs': [],
        'symptoms': [],
        'recommendations': []
    }
    
    # Medical terms detection
    medical_patterns = {
        'medications': r'\b(?:medication|drug|prescription|tablet|capsule|injection|dose|mg|ml)\b',
        'symptoms': r'\b(?:pain|ache|fever|nausea|dizziness|fatigue|weakness|shortness|breath)\b',
        'conditions': r'\b(?:diabetes|hypertension|asthma|pneumonia|infection|inflammation|chronic|acute)\b',
        'vital_signs': r'\b(?:blood pressure|heart rate|temperature|pulse|respiratory rate|oxygen saturation)\b'
    }
    
    text_lower = text.lower()
    
    for category, pattern in medical_patterns.items():
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        insights[category] = list(set(matches))
    
    return insights

def enhance_medical_response(response: str, insights: Dict[str, Any]) -> str:
    """Enhance medical response with additional context"""
    enhanced_response = response
    
    # Add medical disclaimer
    disclaimer = "\n\n⚠️ **Medical Disclaimer**: This information is for educational purposes only and should not be considered as medical advice. Please consult with a qualified healthcare professional for proper diagnosis and treatment."
    
    # Add relevant insights if available
    if insights.get('medications'):
        enhanced_response += f"\n\n💊 **Medications mentioned**: {', '.join(insights['medications'][:3])}"
    
    if insights.get('symptoms'):
        enhanced_response += f"\n\n🩺 **Symptoms identified**: {', '.join(insights['symptoms'][:3])}"
    
    if insights.get('conditions'):
        enhanced_response += f"\n\n🏥 **Conditions discussed**: {', '.join(insights['conditions'][:3])}"
    
    enhanced_response += disclaimer
    
    return enhanced_response 

