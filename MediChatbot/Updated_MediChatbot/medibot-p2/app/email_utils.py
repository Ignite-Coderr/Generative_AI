import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Any, Optional
import json
from datetime import datetime
import streamlit as st
import re
from app.config import EMAIL_CONFIG

def validate_email(email: str) -> bool:
    """Validate email address format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    # return re.match(pattern, email) is not None$'
    return re.match(pattern, email) is not None


def create_medical_analytics_email(user_query: str, 
                                 ai_response: str, 
                                 document_insights: Dict[str, Any],
                                 receiver_email: str,
                                 chat_history: List[Dict] = None) -> MIMEMultipart:
    """Create a comprehensive medical analytics email"""
    
    config = EMAIL_CONFIG
    msg = MIMEMultipart('alternative')
    msg['From'] = config['sender_email']
    msg['To'] = receiver_email
    msg['Subject'] = f"MediChat Pro - Medical Document Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    # Create HTML content
    html_content = generate_html_email_content(
        user_query, ai_response, document_insights, chat_history
    )
    
    # Create plain text content
    text_content = generate_text_email_content(
        user_query, ai_response, document_insights, chat_history
    )
    
    # Attach both versions
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')
    
    msg.attach(part1)
    msg.attach(part2)
    
    return msg


def generate_html_email_content(user_query: str, 
                              ai_response: str, 
                              document_insights: Dict[str, Any],
                              chat_history: List[Dict] = None) -> str:
    """Generate HTML email content"""
    
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #ff4b4b; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .section {{ margin-bottom: 30px; }}
                .section h2 {{ color: #ff4b4b; border-bottom: 2px solid #ff4b4b; padding-bottom: 10px; }}
                .query-box {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #ff4b4b; margin: 15px 0; }}
                .response-box {{ background-color: #e8f5e8; padding: 15px; border-left: 4px solid #28a745; margin: 15px 0; }}
                .insights-box {{ background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 15px 0; }}
                .chat-history {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; }}
                .chat-message {{ margin-bottom: 10px; padding: 10px; border-radius: 5px; }}
                .user-message {{ background-color: #e3f2fd; }}
                .assistant-message {{ background-color: #f3e5f5; }}
                .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #666; }}
                .metric {{ display: inline-block; margin: 10px; padding: 10px; background-color: #e9ecef; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏥 MediChat Pro - Medical Document Analysis</h1>
                <p>Intelligent Medical Document Assistant Report</p>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>📋 Session Summary</h2>
                    <p><strong>Analysis Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Documents Processed:</strong> {document_insights.get('total_documents', 'N/A')}</p>
                    <p><strong>Total Chunks:</strong> {document_insights.get('total_chunks', 'N/A')}</p>
                </div>
                
                <div class="section">
                    <h2>❓ User Query</h2>
                    <div class="query-box">
                        <strong>Question:</strong> {user_query}
                    </div>
                </div>
                
                <div class="section">
                    <h2>🤖 AI Response</h2>
                    <div class="response-box">
                        {ai_response.replace(chr(10), '<br>')}
                    </div>
                </div>
                
                <div class="section">
                    <h2>📊 Document Analytics</h2>
                    <div class="insights-box">
                        <h3>Key Insights:</h3>
                        <ul>
                            <li><strong>Relevant Documents Found:</strong> {document_insights.get('relevant_docs_count', 'N/A')}</li>
                            <li><strong>Confidence Score:</strong> {document_insights.get('confidence_score', 'N/A')}</li>
                            <li><strong>Response Time:</strong> {document_insights.get('response_time', 'N/A')} seconds</li>
                            <li><strong>Query Complexity:</strong> {document_insights.get('query_complexity', 'N/A')}</li>
                        </ul>
                        
                        <h3>Document Coverage:</h3>
                        <p>{document_insights.get('document_coverage', 'Analysis of document coverage not available.')}</p>
                        
                        <h3>Medical Keywords Detected:</h3>
                        <p>{', '.join(document_insights.get('medical_keywords', ['None detected']))}</p>
                    </div>
                </div>
        """
        
    # Add chat history if available
    if chat_history and len(chat_history) > 0:
        html += """
                <div class="section">
                    <h2>💬 Chat History</h2>
                    <div class="chat-history">
            """
        for message in chat_history[-5:]:  # Show last 5 messages
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            timestamp = message.get('timestamp', '')
            
            if role == 'user':
                html += f'<div class="chat-message user-message"><strong>User ({timestamp}):</strong> {content}</div>'
            else:
                html += f'<div class="chat-message assistant-message"><strong>Assistant ({timestamp}):</strong> {content}</div>'
        
        html += """
                </div>
            </div>
        """
        
        html += """
                <div class="section">
                    <h2>🔍 Technical Details</h2>
                    <div class="metric">Model: OpenAI GPT-3.5-Turbo</div>
                    <div class="metric">Embedding: OpenAI text-embedding-ada-002</div>
                    <div class="metric">Vector Store: ChromaDB</div>
                    <div class="metric">Framework: LangChain</div>
                </div>
            </div>
            
            <div class="footer">
                <p>🤖 Powered by OpenAI & LangChain | 🏥 Medical Document Intelligence</p>
                <p>This report was automatically generated by MediChat Pro</p>
            </div>
        </body>
        </html>
        """
        
    return html


def generate_text_email_content(user_query: str, 
                              ai_response: str, 
                              document_insights: Dict[str, Any],
                              chat_history: List[Dict] = None) -> str:
    """Generate plain text email content"""
    
    text = f"""
MEDICHAT PRO - MEDICAL DOCUMENT ANALYSIS REPORT
==============================================

Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Documents Processed: {document_insights.get('total_documents', 'N/A')}
Total Chunks: {document_insights.get('total_chunks', 'N/A')}

USER QUERY:
-----------
{user_query}

AI RESPONSE:
------------
{ai_response}

DOCUMENT ANALYTICS:
------------------
Relevant Documents Found: {document_insights.get('relevant_docs_count', 'N/A')}
Confidence Score: {document_insights.get('confidence_score', 'N/A')}
Response Time: {document_insights.get('response_time', 'N/A')} seconds
Query Complexity: {document_insights.get('query_complexity', 'N/A')}

Document Coverage:
{document_insights.get('document_coverage', 'Analysis of document coverage not available.')}

Medical Keywords Detected:
{', '.join(document_insights.get('medical_keywords', ['None detected']))}
        """
        
    if chat_history and len(chat_history) > 0:
        text += "\n\nCHAT HISTORY:\n------------\n"
        for message in chat_history[-5:]:
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            timestamp = message.get('timestamp', '')
            text += f"{role.upper()} ({timestamp}): {content}\n"
        
        text += """
TECHNICAL DETAILS:
-----------------
Model: OpenAI GPT-3.5-Turbo
Embedding: OpenAI text-embedding-ada-002
Vector Store: ChromaDB
Framework: LangChain

---
🤖 Powered by OpenAI & LangChain | 🏥 Medical Document Intelligence
This report was automatically generated by MediChat Pro
        """
        
    return text


def send_email(message: MIMEMultipart) -> bool:
    """Send email using SMTP with enhanced error handling"""
    try:
        config = EMAIL_CONFIG
        
        # Validate configuration
        if not config['sender_email'] or not config['sender_password']:
            st.error("❌ Email configuration is incomplete. Please check EMAIL_SENDER and EMAIL_PASSWORD in .env file.")
            return False
        
        if not config['smtp_server'] or not config['smtp_port']:
            st.error("❌ SMTP configuration is incomplete. Please check EMAIL_SMTP_SERVER and EMAIL_SMTP_PORT in .env file.")
            return False
        
        # Create secure connection with better error handling
        context = ssl.create_default_context()
        
        # Try to connect and send email
        try:
            with smtplib.SMTP(config['smtp_server'], config['smtp_port']) as server:
                # Enable debug mode for troubleshooting (remove in production)
                # server.set_debuglevel(1)
                
                # Start TLS encryption
                server.starttls(context=context)
                
                # Login with credentials
                server.login(config['sender_email'], config['sender_password'])
                
                # Send the message
                text = message.as_string()
                server.sendmail(config['sender_email'], message['To'], text)
                
            st.success("✅ Email sent successfully!")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            st.error(f"❌ Email authentication failed: {str(e)}")
            st.error("💡 Check your Gmail app password. Make sure 2FA is enabled and you're using an app password, not your regular password.")
            return False
            
        except smtplib.SMTPRecipientsRefused as e:
            st.error(f"❌ Recipient email refused: {str(e)}")
            st.error("💡 Check if the recipient email address is valid.")
            return False
            
        except smtplib.SMTPServerDisconnected as e:
            st.error(f"❌ SMTP server disconnected: {str(e)}")
            st.error("💡 Check your internet connection and SMTP server settings.")
            return False
            
        except smtplib.SMTPException as e:
            st.error(f"❌ SMTP error: {str(e)}")
            return False
            
    except Exception as e:
        st.error(f"❌ Failed to send email: {str(e)}")
        st.error("💡 Common fixes:")
        st.error("   • Check internet connection")
        st.error("   • Verify Gmail app password (not regular password)")
        st.error("   • Ensure 2-factor authentication is enabled")
        st.error("   • Check if 'Less secure app access' is disabled (use app password instead)")
        return False


def send_medical_analytics(user_query: str, 
                         ai_response: str, 
                         document_insights: Dict[str, Any],
                         receiver_email: str,
                         chat_history: List[Dict] = None) -> bool:
    """Send medical analytics email"""
    try:
        message = create_medical_analytics_email(
            user_query, ai_response, document_insights, receiver_email, chat_history
        )
        return send_email(message)
    except Exception as e:
        st.error(f"Failed to create or send medical analytics email: {str(e)}")
        return False


def create_support_ticket_email(user_query: str, 
                              ai_response: str, 
                              user_email: str = None,
                              chat_history: List[Dict] = None) -> MIMEMultipart:
    """Create a support ticket email"""
    
    config = EMAIL_CONFIG
    msg = MIMEMultipart('alternative')
    msg['From'] = config['sender_email']
    msg['To'] = 'amanhusain8899@gmail.com'  # Support email
    msg['Subject'] = f"MediChat Pro Support Ticket - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    # Create HTML content
    html_content = generate_support_ticket_html_content(
        user_query, ai_response, user_email, chat_history
    )
    
    # Create plain text content
    text_content = generate_support_ticket_text_content(
        user_query, ai_response, user_email, chat_history
    )
    
    # Attach both versions
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')
    
    msg.attach(part1)
    msg.attach(part2)
    
    return msg


def generate_support_ticket_html_content(user_query: str, 
                                       ai_response: str, 
                                       user_email: str = None,
                                       chat_history: List[Dict] = None) -> str:
    """Generate HTML content for support ticket"""
    
    # Generate comprehensive ticket information
    ticket_id = f"MC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
            .header {{ background-color: #ff4b4b; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; max-width: 800px; margin: 0 auto; }}
            .section {{ margin-bottom: 30px; border: 1px solid #ddd; border-radius: 8px; padding: 20px; }}
            .section h2 {{ color: #ff4b4b; border-bottom: 2px solid #ff4b4b; padding-bottom: 10px; margin-top: 0; }}
            .query-box {{ background-color: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; margin: 15px 0; border-radius: 5px; }}
            .response-box {{ background-color: #e8f5e8; padding: 15px; border-left: 4px solid #28a745; margin: 15px 0; border-radius: 5px; }}
            .support-info {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #17a2b8; margin: 15px 0; border-radius: 5px; }}
            .chat-history {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; max-height: 400px; overflow-y: auto; }}
            .chat-message {{ margin-bottom: 10px; padding: 10px; border-radius: 5px; }}
            .user-message {{ background-color: #e3f2fd; border-left: 3px solid #2196f3; }}
            .assistant-message {{ background-color: #f3e5f5; border-left: 3px solid #9c27b0; }}
            .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #666; margin-top: 30px; }}
            .priority {{ display: inline-block; margin: 10px; padding: 8px 15px; background-color: #ffc107; border-radius: 20px; color: #000; font-weight: bold; }}
            .info-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }}
            .info-item {{ background-color: #f8f9fa; padding: 10px; border-radius: 5px; }}
            .info-label {{ font-weight: bold; color: #555; }}
            .info-value {{ color: #333; }}
            .urgent {{ background-color: #dc3545; color: white; }}
            .stats {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎫 MediChat Pro Support Ticket</h1>
            <p>Comprehensive User Support Request</p>
            <p><strong>Ticket ID: {ticket_id}</strong></p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📋 Ticket Information</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <div class="info-label">Ticket ID:</div>
                        <div class="info-value">{ticket_id}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Created:</div>
                        <div class="info-value">{timestamp}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Priority:</div>
                        <div class="info-value"><span class="priority">HIGH</span></div>
                    </div>
                    <div class="info-item">
                        <div class="info-label">Category:</div>
                        <div class="info-value">Medical AI Support</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>👤 User Information</h2>
                <div class="support-info">
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-label">User Email:</div>
                            <div class="info-value">{user_email if user_email else 'Not provided'}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Platform:</div>
                            <div class="info-value">MediChat Pro Web Application</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">Session Time:</div>
                            <div class="info-value">{timestamp}</div>
                        </div>
                        <div class="info-item">
                            <div class="info-label">User Agent:</div>
                            <div class="info-value">Streamlit Web App</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>❓ User Query Details</h2>
                <div class="query-box">
                    <div class="info-label">Original Question:</div>
                    <div style="margin-top: 10px; font-size: 16px; line-height: 1.5;">
                        {user_query if user_query else 'No query provided'}
                    </div>
                </div>
                <div class="stats">
                    <strong>Query Statistics:</strong><br>
                    • Length: {len(user_query) if user_query else 0} characters<br>
                    • Word Count: {len(user_query.split()) if user_query else 0} words<br>
                    • Type: {'Medical Query' if any(word in user_query.lower() for word in ['medical', 'health', 'doctor', 'patient', 'symptom', 'diagnosis', 'treatment'] if user_query) else 'General Query'}
                </div>
            </div>
            
            <div class="section">
                <h2>🤖 AI Response Details</h2>
                <div class="response-box">
                    <div class="info-label">AI Generated Response:</div>
                    <div style="margin-top: 10px; font-size: 16px; line-height: 1.5;">
                        {ai_response.replace(chr(10), '<br>') if ai_response else 'No response provided'}
                    </div>
                </div>
                <div class="stats">
                    <strong>Response Statistics:</strong><br>
                    • Length: {len(ai_response) if ai_response else 0} characters<br>
                    • Word Count: {len(ai_response.split()) if ai_response else 0} words<br>
                    • Model: Euron API - gpt-4.1-nano<br>
                    • Generated: {timestamp}
                </div>
            </div>
    """
    
    # Add comprehensive chat history if available
    if chat_history and len(chat_history) > 0:
        html += f"""
            <div class="section">
                <h2>💬 Complete Chat History ({len(chat_history)} messages)</h2>
                <div class="stats">
                    <strong>Session Statistics:</strong><br>
                    • Total Messages: {len(chat_history)}<br>
                    • User Messages: {len([m for m in chat_history if m.get('role') == 'user'])}<br>
                    • Assistant Messages: {len([m for m in chat_history if m.get('role') == 'assistant'])}<br>
                    • Session Duration: Active session
                </div>
                <div class="chat-history">
        """
        
        for i, message in enumerate(chat_history[-15:], 1):  # Show last 15 messages
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            timestamp_msg = message.get('timestamp', f'Message {i}')
            
            if role == 'user':
                html += f'''
                <div class="chat-message user-message">
                    <strong>👤 User ({timestamp_msg}):</strong><br>
                    <div style="margin-top: 5px;">{content}</div>
                </div>'''
            else:
                html += f'''
                <div class="chat-message assistant-message">
                    <strong>🤖 Assistant ({timestamp_msg}):</strong><br>
                    <div style="margin-top: 5px;">{content}</div>
                </div>'''
        
        html += """
                </div>
            </div>
        """
    else:
        html += """
            <div class="section">
                <h2>💬 Chat History</h2>
                <div class="support-info">
                    <p><strong>No chat history available</strong> - This appears to be a standalone query.</p>
                </div>
            </div>
        """
    
    html += f"""
            <div class="section">
                <h2>🔍 Support Analysis & Action Items</h2>
                <div class="support-info">
                    <h3>📊 Automatic Analysis:</h3>
                    <ul>
                        <li><strong>Query Type:</strong> {'Medical/Health Related' if user_query and any(word in user_query.lower() for word in ['medical', 'health', 'doctor', 'patient', 'symptom', 'diagnosis', 'treatment']) else 'General Support'}</li>
                        <li><strong>Complexity:</strong> {'High' if user_query and len(user_query.split()) > 20 else 'Medium' if user_query and len(user_query.split()) > 10 else 'Low'}</li>
                        <li><strong>Response Quality:</strong> {'Comprehensive' if ai_response and len(ai_response) > 200 else 'Standard' if ai_response and len(ai_response) > 50 else 'Brief'}</li>
                        <li><strong>User Engagement:</strong> {'High' if chat_history and len(chat_history) > 5 else 'Medium' if chat_history and len(chat_history) > 2 else 'Low'}</li>
                    </ul>
                    
                    <h3>⚡ Recommended Actions:</h3>
                    <ul>
                        <li>✅ Review the AI response for accuracy and completeness</li>
                        <li>✅ Check if the user query was fully addressed</li>
                        <li>✅ Verify medical information if health-related</li>
                        <li>✅ Follow up with user if response seems insufficient</li>
                        <li>✅ Document any improvements needed for AI training</li>
                    </ul>
                    
                    <h3>📞 Contact Information:</h3>
                    <ul>
                        <li><strong>User Email:</strong> {user_email if user_email else 'Not provided - contact via app'}</li>
                        <li><strong>Ticket ID:</strong> {ticket_id}</li>
                        <li><strong>Created:</strong> {timestamp}</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <h3>🎫 MediChat Pro Support System</h3>
            <p><strong>Automated Ticket Generation</strong> | <strong>Ticket ID:</strong> {ticket_id}</p>
            <p>This comprehensive support ticket was automatically generated by the MediChat Pro application</p>
            <p><em>For urgent medical emergencies, please contact emergency services immediately</em></p>
        </div>
    </body>
    </html>
    """
    
    return html


def generate_support_ticket_text_content(user_query: str, 
                                       ai_response: str, 
                                       user_email: str = None,
                                       chat_history: List[Dict] = None) -> str:
    """Generate plain text content for support ticket"""
    
    ticket_id = f"MC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    text = f"""
MEDICHAT PRO SUPPORT TICKET - COMPREHENSIVE REPORT
==================================================

TICKET INFORMATION:
------------------
Ticket ID: {ticket_id}
Created: {timestamp}
Priority: HIGH
Category: Medical AI Support
Status: NEW - Requires Review

USER INFORMATION:
----------------
User Email: {user_email if user_email else 'Not provided'}
Platform: MediChat Pro Web Application
Session Time: {timestamp}
User Agent: Streamlit Web App

USER QUERY DETAILS:
------------------
Original Question: {user_query if user_query else 'No query provided'}

Query Statistics:
• Length: {len(user_query) if user_query else 0} characters
• Word Count: {len(user_query.split()) if user_query else 0} words
• Type: {'Medical Query' if user_query and any(word in user_query.lower() for word in ['medical', 'health', 'doctor', 'patient', 'symptom', 'diagnosis', 'treatment']) else 'General Query'}
• Complexity: {'High' if user_query and len(user_query.split()) > 20 else 'Medium' if user_query and len(user_query.split()) > 10 else 'Low'}

AI RESPONSE DETAILS:
-------------------
AI Generated Response: {ai_response if ai_response else 'No response provided'}

Response Statistics:
• Length: {len(ai_response) if ai_response else 0} characters
• Word Count: {len(ai_response.split()) if ai_response else 0} words
• Model: Euron API - gpt-4.1-nano
• Generated: {timestamp}
• Quality: {'Comprehensive' if ai_response and len(ai_response) > 200 else 'Standard' if ai_response and len(ai_response) > 50 else 'Brief'}
    """
    
    if chat_history and len(chat_history) > 0:
        text += f"""
COMPLETE CHAT HISTORY ({len(chat_history)} messages):
--------------------------------------------------
Session Statistics:
• Total Messages: {len(chat_history)}
• User Messages: {len([m for m in chat_history if m.get('role') == 'user'])}
• Assistant Messages: {len([m for m in chat_history if m.get('role') == 'assistant'])}
• User Engagement: {'High' if len(chat_history) > 5 else 'Medium' if len(chat_history) > 2 else 'Low'}

Chat Messages (Last 15):
"""
        for i, message in enumerate(chat_history[-15:], 1):
            role = message.get('role', 'unknown')
            content = message.get('content', '')
            timestamp_msg = message.get('timestamp', f'Message {i}')
            text += f"\n{i}. {role.upper()} ({timestamp_msg}):\n   {content}\n"
    else:
        text += """
CHAT HISTORY:
------------
No chat history available - This appears to be a standalone query.
"""
    
    text += f"""
SUPPORT ANALYSIS & ACTION ITEMS:
-------------------------------
Automatic Analysis:
• Query Type: {'Medical/Health Related' if user_query and any(word in user_query.lower() for word in ['medical', 'health', 'doctor', 'patient', 'symptom', 'diagnosis', 'treatment']) else 'General Support'}
• Complexity: {'High' if user_query and len(user_query.split()) > 20 else 'Medium' if user_query and len(user_query.split()) > 10 else 'Low'}
• Response Quality: {'Comprehensive' if ai_response and len(ai_response) > 200 else 'Standard' if ai_response and len(ai_response) > 50 else 'Brief'}
• User Engagement: {'High' if chat_history and len(chat_history) > 5 else 'Medium' if chat_history and len(chat_history) > 2 else 'Low'}

Recommended Actions:
✓ Review the AI response for accuracy and completeness
✓ Check if the user query was fully addressed
✓ Verify medical information if health-related
✓ Follow up with user if response seems insufficient
✓ Document any improvements needed for AI training

Contact Information:
• User Email: {user_email if user_email else 'Not provided - contact via app'}
• Ticket ID: {ticket_id}
• Created: {timestamp}

SYSTEM INFORMATION:
------------------
• Application: MediChat Pro Web Application
• AI Model: Euron API - gpt-4.1-nano
• Platform: Streamlit
• Ticket Generation: Automated
• Priority Level: HIGH (Medical AI Support)

---
🎫 MEDICHAT PRO SUPPORT SYSTEM | 🤖 AUTOMATED TICKET GENERATION
Ticket ID: {ticket_id} | Created: {timestamp}
This comprehensive support ticket was automatically generated by the MediChat Pro application.

⚠️ IMPORTANT: For urgent medical emergencies, please contact emergency services immediately.
    """
    
    return text


def send_support_ticket(user_query: str, 
                       ai_response: str, 
                       user_email: str = None,
                       chat_history: List[Dict] = None) -> bool:
    """Send support ticket email"""
    try:
        message = create_support_ticket_email(
            user_query, ai_response, user_email, chat_history
        )
        return send_email(message)
    except Exception as e:
        st.error(f"Failed to create or send support ticket: {str(e)}")
        return False


def generate_document_insights(vectorstore, user_query: str, ai_response: str, 
                             relevant_docs: List, response_time: float) -> Dict[str, Any]:
    """Generate insights from document analysis"""
    
    # Extract medical keywords (basic implementation)
    medical_keywords = []
    medical_terms = [
        'diagnosis', 'treatment', 'medication', 'symptom', 'condition', 'disease',
        'therapy', 'prescription', 'allergy', 'blood pressure', 'heart rate',
        'temperature', 'pain', 'inflammation', 'infection', 'chronic', 'acute',
        'patient', 'doctor', 'nurse', 'hospital', 'clinic', 'medical', 'health'
    ]
    
    query_lower = user_query.lower()
    response_lower = ai_response.lower()
    
    for term in medical_terms:
        if term in query_lower or term in response_lower:
            medical_keywords.append(term)
    
    # Calculate confidence score based on response length and medical keywords
    confidence_score = min(100, (len(medical_keywords) * 10) + (len(ai_response) / 10))
    
    # Determine query complexity
    query_complexity = "Simple"
    if len(user_query.split()) > 10:
        query_complexity = "Complex"
    elif len(user_query.split()) > 5:
        query_complexity = "Medium"
    
    # Document coverage analysis
    doc_coverage = f"Analysis covered {len(relevant_docs)} relevant document chunks"
    if len(relevant_docs) > 3:
        doc_coverage += " with comprehensive coverage."
    elif len(relevant_docs) > 1:
        doc_coverage += " with moderate coverage."
    else:
        doc_coverage += " with limited coverage."
    
    return {
        'total_documents': 'Multiple',  # This would need to be tracked from session
        'total_chunks': len(relevant_docs) * 2,  # Estimate
        'relevant_docs_count': len(relevant_docs),
        'confidence_score': f"{confidence_score:.1f}%",
        'response_time': f"{response_time:.2f}",
        'query_complexity': query_complexity,
        'document_coverage': doc_coverage,
        'medical_keywords': medical_keywords[:10]  # Limit to top 10
    }

def generate_session_insights(chat_history: List, document_count: int) -> Dict[str, Any]:
    """Generate insights from chat session for reports"""
    
    # Analyze chat history
    total_messages = len(chat_history)
    user_messages = [msg for msg in chat_history if msg.get('role') == 'user']
    assistant_messages = [msg for msg in chat_history if msg.get('role') == 'assistant']
    
    # Extract medical keywords from all messages
    medical_keywords = []
    medical_terms = [
        'diagnosis', 'treatment', 'medication', 'symptom', 'condition', 'disease',
        'therapy', 'prescription', 'allergy', 'blood pressure', 'heart rate',
        'temperature', 'pain', 'inflammation', 'infection', 'chronic', 'acute',
        'patient', 'doctor', 'nurse', 'hospital', 'clinic', 'medical', 'health'
    ]
    
    all_text = ' '.join([msg.get('content', '') for msg in chat_history]).lower()
    
    for term in medical_terms:
        if term in all_text:
            medical_keywords.append(term)
    
    # Calculate session metrics
    avg_response_length = sum(len(msg.get('content', '')) for msg in assistant_messages) / max(len(assistant_messages), 1)
    
    return {
        'total_documents': document_count,
        'total_chunks': total_messages,
        'relevant_docs_count': len(assistant_messages),
        'confidence_score': f"{min(100, len(medical_keywords) * 5 + document_count * 10):.1f}%",
        'response_time': '0.00',
        'query_complexity': 'Session Analysis',
        'document_coverage': f"Session with {document_count} documents and {total_messages} messages analyzed.",
        'medical_keywords': list(set(medical_keywords))[:10]  # Unique keywords, limit to 10
    }


