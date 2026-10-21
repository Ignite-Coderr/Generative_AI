import os
from dotenv import load_dotenv
import warnings

# Load environment variables
load_dotenv()

# OpenAI API Configuration
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDING_BASE = os.getenv("OPENAI_EMBEDDING_BASE", "https://api.openai.com/v1")
OPENAI_EMBEDDING_KEY = os.getenv("OPENAI_EMBEDDING_KEY")

# Model Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com"),
    'smtp_port': int(os.getenv("EMAIL_SMTP_PORT", "587")),
    'sender_email': os.getenv("EMAIL_SENDER"),
    'sender_password': os.getenv("EMAIL_PASSWORD"),
    'receiver_email': os.getenv("EMAIL_RECEIVER", "sudhanshu@euron.one")
}

# ChromaDB Configuration
CHROMA_CONFIG = {
    'api_key': os.getenv("CHROMA_API_KEY"),
    'tenant': os.getenv("CHROMA_TENANT"),
    'database': os.getenv("CHROMA_DATABASE", "medibot"),
    'collection': os.getenv("CHROMA_COLLECTION", "medical_documents")
}

# AWS S3 Configuration
S3_CONFIG = {
    'access_key': os.getenv("S3_ACCESS_KEY"),
    'secret_key': os.getenv("S3_SECRET_KEY"),
    'bucket_name': os.getenv("S3_BUCKET_NAME"),
    'region': os.getenv("S3_REGION", "us-east-1")
}

# Application Configuration
APP_CONFIG = {
    'debug': os.getenv("DEBUG", "False").lower() == "true",
    'log_level': os.getenv("LOG_LEVEL", "INFO"),
    'max_file_size': int(os.getenv("MAX_FILE_SIZE", "10485760")),  # 10MB default
    'supported_file_types': os.getenv("SUPPORTED_FILE_TYPES", "pdf,txt,docx").split(","),
    'session_timeout': int(os.getenv("SESSION_TIMEOUT", "3600")),  # 1 hour default
}

# Validation function to check if required environment variables are set
def validate_config():
    """Validate that required environment variables are set"""
    required_vars = {
        'OPENAI_API_KEY': OPENAI_API_KEY,
        'OPENAI_EMBEDDING_KEY': OPENAI_EMBEDDING_KEY
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Validate API key format (updated for Euron API)
    if OPENAI_API_KEY and not (OPENAI_API_KEY.startswith(('sk-', 'sk-proj-')) or OPENAI_API_KEY.startswith('euri-')):
        warnings.warn("API key format may be incorrect. Should start with 'sk-', 'sk-proj-', or 'euri-' for Euron API")
    
    return True

# Optional validation for email functionality
def validate_email_config():
    """Validate email configuration"""
    if not EMAIL_CONFIG['sender_email'] or not EMAIL_CONFIG['sender_password']:
        return False
    
    # Basic email format validation
    import re
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if EMAIL_CONFIG['sender_email'] and not re.match(email_pattern, EMAIL_CONFIG['sender_email']):
        warnings.warn(f"Email format may be incorrect: {EMAIL_CONFIG['sender_email']}")
        return False
    
    return True

# Optional validation for ChromaDB functionality
def validate_chroma_config():
    """Validate ChromaDB configuration"""
    if not CHROMA_CONFIG['api_key'] or not CHROMA_CONFIG['tenant']:
        return False
    
    # Validate ChromaDB API key format
    if CHROMA_CONFIG['api_key'] and not CHROMA_CONFIG['api_key'].startswith('ck-'):
        warnings.warn("ChromaDB API key format may be incorrect. Should start with 'ck-'")
    
    return True

# Optional validation for S3 functionality
def validate_s3_config():
    """Validate S3 configuration"""
    if not S3_CONFIG['access_key'] or not S3_CONFIG['secret_key'] or not S3_CONFIG['bucket_name']:
        return False
    
    # Validate AWS access key format
    if S3_CONFIG['access_key'] and not S3_CONFIG['access_key'].startswith('AKIA'):
        warnings.warn("AWS Access Key format may be incorrect. Should start with 'AKIA'")
    
    return True

def get_config_status():
    """Get overall configuration status"""
    status = {
        'openai': False,
        'email': False,
        'chroma': False,
        's3': False,
        'errors': [],
        'warnings': []
    }
    
    try:
        validate_config()
        status['openai'] = True
    except Exception as e:
        status['errors'].append(f"OpenAI: {str(e)}")
    
    try:
        status['email'] = validate_email_config()
    except Exception as e:
        status['warnings'].append(f"Email: {str(e)}")
    
    try:
        status['chroma'] = validate_chroma_config()
    except Exception as e:
        status['warnings'].append(f"ChromaDB: {str(e)}")
    
    try:
        status['s3'] = validate_s3_config()
    except Exception as e:
        status['warnings'].append(f"S3: {str(e)}")
    
    return status

def print_config_summary():
    """Print a summary of the current configuration"""
    print("🔧 MediChatbot Configuration Summary")
    print("=" * 40)
    
    status = get_config_status()
    
    print(f"OpenAI API: {'✅ Configured' if status['openai'] else '❌ Missing'}")
    print(f"Email: {'✅ Configured' if status['email'] else '⚠️  Optional'}")
    print(f"ChromaDB: {'✅ Configured' if status['chroma'] else '⚠️  Optional'}")
    print(f"S3 Storage: {'✅ Configured' if status['s3'] else '⚠️  Optional'}")
    
    if status['errors']:
        print("\n❌ Errors:")
        for error in status['errors']:
            print(f"  - {error}")
    
    if status['warnings']:
        print("\n⚠️  Warnings:")
        for warning in status['warnings']:
            print(f"  - {warning}")
    
    print(f"\nModels:")
    print(f"  - LLM: {LLM_MODEL}")
    print(f"  - Embedding: {EMBEDDING_MODEL}")
    
    return status

# Auto-validate on import (optional)
if os.getenv("AUTO_VALIDATE_CONFIG", "false").lower() == "true":
    try:
        validate_config()
        print("✅ Configuration validated successfully")
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")

# Export commonly used configurations
__all__ = [
    'OPENAI_API_KEY', 'OPENAI_API_BASE', 'OPENAI_EMBEDDING_KEY', 'OPENAI_EMBEDDING_BASE',
    'LLM_MODEL', 'EMBEDDING_MODEL',
    'EMAIL_CONFIG', 'CHROMA_CONFIG', 'S3_CONFIG', 'APP_CONFIG',
    'validate_config', 'validate_email_config', 'validate_chroma_config', 'validate_s3_config',
    'get_config_status', 'print_config_summary'
]