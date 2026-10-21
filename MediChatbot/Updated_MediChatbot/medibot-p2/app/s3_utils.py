"""
S3 Document Storage Utilities - Function-based implementation
"""

import boto3
import hashlib
import os
from typing import List, Optional, Dict, Any
from botocore.exceptions import ClientError, NoCredentialsError
import streamlit as st
from app.pdf_utils import clean_text
from app.config import S3_CONFIG
import time

def get_s3_client():
    """Get S3 client with credentials"""
    try:
        if not S3_CONFIG['access_key'] or not S3_CONFIG['secret_key']:
            print("⚠️ S3 credentials not configured")
            return None
            
        s3_client = boto3.client(
            's3',
            aws_access_key_id=S3_CONFIG['access_key'],
            aws_secret_access_key=S3_CONFIG['secret_key'],
            region_name=S3_CONFIG['region']
        )
        return s3_client
    except Exception as e:
        print(f"❌ Error creating S3 client: {e}")
        return None

def generate_document_key(filename: str, content: str) -> str:
    """Generate unique S3 key for document"""
    # Create hash of content for uniqueness
    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    # Clean filename
    clean_filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
    # Generate key
    key = f"documents/{content_hash}_{clean_filename}"
    return key

def upload_document_to_s3(file_content: bytes, filename: str, content_text: str) -> Dict[str, Any]:
    """Upload document to S3 bucket"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return {'success': False, 'error': 'Failed to create S3 client'}
        
        # Generate unique key
        key = generate_document_key(filename, content_text)
        
        # Upload to S3
        s3_client.put_object(
            Bucket=S3_CONFIG['bucket_name'],
            Key=key,
            Body=file_content,
            ContentType='application/pdf',
            Metadata={
                'filename': filename,
                'content_hash': hashlib.md5(content_text.encode()).hexdigest(),
                'upload_timestamp': str(int(time.time()))
            }
        )
        
        print(f"✅ Document uploaded to S3: s3://{S3_CONFIG['bucket_name']}/{key}")
        
        return {
            'success': True,
            's3_key': key,
            's3_url': f"s3://{S3_CONFIG['bucket_name']}/{key}",
            'filename': filename
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"❌ S3 Client Error: {error_code} - {e}")
        return {'success': False, 'error': f'S3 Error: {error_code}'}
    except NoCredentialsError:
        print("❌ AWS credentials not found")
        return {'success': False, 'error': 'AWS credentials not found'}
    except Exception as e:
        print(f"❌ Error uploading to S3: {e}")
        return {'success': False, 'error': str(e)}

def list_documents_in_s3() -> List[Dict[str, Any]]:
    """List all documents in S3 bucket"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return []
        
        response = s3_client.list_objects_v2(
            Bucket=S3_CONFIG['bucket_name'],
            Prefix='documents/'
        )
        
        documents = []
        if 'Contents' in response:
            for obj in response['Contents']:
                # Get object metadata
                try:
                    metadata_response = s3_client.head_object(
                        Bucket=S3_CONFIG['bucket_name'],
                        Key=obj['Key']
                    )
                    metadata = metadata_response.get('Metadata', {})
                except:
                    metadata = {}
                
                documents.append({
                    'key': obj['Key'],
                    'filename': metadata.get('filename', obj['Key'].split('/')[-1]),
                    'size': obj['Size'],
                    'last_modified': obj['LastModified'],
                    's3_url': f"s3://{S3_CONFIG['bucket_name']}/{obj['Key']}"
                })
        
        print(f"📄 Found {len(documents)} documents in S3 bucket")
        return documents
        
    except Exception as e:
        print(f"❌ Error listing S3 documents: {e}")
        return []

def download_document_from_s3(s3_key: str) -> Dict[str, Any]:
    """Download document from S3"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return {'success': False, 'error': 'Failed to create S3 client'}
        
        response = s3_client.get_object(
            Bucket=S3_CONFIG['bucket_name'],
            Key=s3_key
        )
        
        file_content = response['Body'].read()
        metadata = response.get('Metadata', {})
        
        return {
            'success': True,
            'content': file_content,
            'filename': metadata.get('filename', s3_key.split('/')[-1]),
            'content_type': response.get('ContentType', 'application/pdf')
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"❌ S3 Download Error: {error_code} - {e}")
        return {'success': False, 'error': f'S3 Error: {error_code}'}
    except Exception as e:
        print(f"❌ Error downloading from S3: {e}")
        return {'success': False, 'error': str(e)}

def check_document_exists_in_s3(filename: str, content_text: str) -> Dict[str, Any]:
    """Check if document already exists in S3"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return {'exists': False, 'error': 'Failed to create S3 client'}
        
        # Generate the same key that would be used for upload
        key = generate_document_key(filename, content_text)
        
        try:
            s3_client.head_object(
                Bucket=S3_CONFIG['bucket_name'],
                Key=key
            )
            return {
                'exists': True,
                's3_key': key,
                's3_url': f"s3://{S3_CONFIG['bucket_name']}/{key}"
            }
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return {'exists': False}
            else:
                return {'exists': False, 'error': str(e)}
                
    except Exception as e:
        print(f"❌ Error checking S3 document: {e}")
        return {'exists': False, 'error': str(e)}

def delete_document_from_s3(s3_key: str) -> Dict[str, Any]:
    """Delete document from S3"""
    try:
        s3_client = get_s3_client()
        if not s3_client:
            return {'success': False, 'error': 'Failed to create S3 client'}
        
        s3_client.delete_object(
            Bucket=S3_CONFIG['bucket_name'],
            Key=s3_key
        )
        
        print(f"🗑️ Document deleted from S3: {s3_key}")
        return {'success': True}
        
    except Exception as e:
        print(f"❌ Error deleting from S3: {e}")
        return {'success': False, 'error': str(e)}

def process_uploaded_files_with_s3(uploaded_files: List, extract_text_func) -> Dict[str, Any]:
    """Process uploaded files and store in S3"""
    try:
        results = {
            'uploaded_to_s3': [],
            'already_in_s3': [],
            'failed_uploads': [],
            'all_texts': []
        }
        
        for uploaded_file in uploaded_files:
            try:
                # Read file content
                file_content = uploaded_file.read()
                filename = uploaded_file.name
                
                # Extract text for processing
                from io import BytesIO
                file_like = BytesIO(file_content)
                text_content = clean_text(extract_text_func(file_like))
                
                # Check if document already exists in S3
                s3_check = check_document_exists_in_s3(filename, text_content)
                
                if s3_check.get('exists', False):
                    print(f"📄 Document already exists in S3: {filename}")
                    results['already_in_s3'].append({
                        'filename': filename,
                        's3_key': s3_check['s3_key'],
                        's3_url': s3_check['s3_url']
                    })
                else:
                    # Upload to S3
                    upload_result = upload_document_to_s3(file_content, filename, text_content)
                    
                    if upload_result['success']:
                        print(f"✅ Document uploaded to S3: {filename}")
                        results['uploaded_to_s3'].append({
                            'filename': filename,
                            's3_key': upload_result['s3_key'],
                            's3_url': upload_result['s3_url']
                        })
                    else:
                        print(f"❌ Failed to upload to S3: {filename}")
                        results['failed_uploads'].append({
                            'filename': filename,
                            'error': upload_result['error']
                        })
                
                # Add text content for vector processing
                results['all_texts'].append(text_content)
                
            except Exception as e:
                print(f"❌ Error processing file {uploaded_file.name}: {e}")
                results['failed_uploads'].append({
                    'filename': uploaded_file.name,
                    'error': str(e)
                })
        
        return results
        
    except Exception as e:
        print(f"❌ Error in process_uploaded_files_with_s3: {e}")
        return {
            'uploaded_to_s3': [],
            'already_in_s3': [],
            'failed_uploads': [],
            'all_texts': [],
            'error': str(e)
        }

def get_s3_documents_for_vector_processing() -> List[Dict[str, Any]]:
    """Get S3 documents that can be processed for vector storage"""
    try:
        s3_documents = list_documents_in_s3()
        return s3_documents
    except Exception as e:
        print(f"❌ Error getting S3 documents: {e}")
        return []

def process_all_s3_documents_for_vector_storage(extract_text_func):
    """Process all S3 documents for vector storage"""
    try:
        print("🔄 Processing all S3 documents for vector storage...")
        
        # Get all S3 documents
        s3_docs = list_documents_in_s3()
        if not s3_docs:
            print("📂 No documents found in S3")
            return []
        
        print(f"📄 Found {len(s3_docs)} documents in S3 to process")
        
        all_texts = []
        processed_count = 0
        
        for doc in s3_docs:
            try:
                print(f"📥 Downloading: {doc['filename']}")
                
                # Download document from S3
                download_result = download_document_from_s3(doc['key'])
                
                if download_result['success']:
                    # Extract text from downloaded content
                    from io import BytesIO
                    file_like = BytesIO(download_result['content'])
                    text_content = clean_text(extract_text_func(file_like))
                    
                    if text_content and text_content.strip():
                        all_texts.append(text_content)
                        processed_count += 1
                        print(f"✅ Processed: {doc['filename']}")
                    else:
                        print(f"⚠️ No text extracted from: {doc['filename']}")
                else:
                    print(f"❌ Failed to download: {doc['filename']} - {download_result['error']}")
                    
            except Exception as e:
                print(f"❌ Error processing {doc['filename']}: {e}")
                continue
        
        print(f"🎉 Successfully processed {processed_count}/{len(s3_docs)} S3 documents")
        return all_texts
        
    except Exception as e:
        print(f"❌ Error in process_all_s3_documents_for_vector_storage: {e}")
        return []

# Remove the duplicate import at the end
