"""
Gmail Sender MCP Server
A Model Context Protocol server that provides access to Gmail sending capabilities through tools.
"""
import os
import base64
from email.mime.text import MIMEText

# Environment and authentication
import dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# MCP imports
from mcp.server.fastmcp import FastMCP

# Load environment variables
dotenv.load_dotenv()

# API setup
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
]

def get_credentials():
    """Set up and return the Google API credentials using environment variables."""
    # Get credentials from environment variables
    client_id = os.getenv('GMAIL_CLIENT_ID')
    client_secret = os.getenv('GMAIL_CLIENT_SECRET')
    refresh_token = os.getenv('GMAIL_REFRESH_TOKEN')
    
    # Check if all required credentials are available
    if not all([client_id, client_secret, refresh_token]):
        raise ValueError("Missing Google API credentials in environment variables. "
                         "Please set GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, and GMAIL_REFRESH_TOKEN.")
    
    # Create credentials object
    creds = Credentials(
        None,  # No access token - it will be obtained via refresh
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=SCOPES
    )
    
    # Refresh the token to get a valid access token
    creds.refresh(Request())
    return creds

def get_gmail_service():
    """Set up and return the Gmail API service."""
    return build('gmail', 'v1', credentials=get_credentials())

# Initialize the MCP server
mcp = FastMCP("Gmail Sender MCP Server")

# ================== GMAIL TOOLS ==================

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """
    Send an email using Gmail.
    
    Args:
        to: Email recipient address
        subject: Email subject line
        body: Plain text email body content
    """
    service = get_gmail_service()
    
    # Create the email message
    message = MIMEText(body, 'html')
    message['to'] = to
    message['subject'] = subject
    
    # Set sender if specified in environment
    user_email = os.getenv('GMAIL_USER_EMAIL')
    if user_email:
        message['from'] = user_email
    
    # Encode the message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    # Send the message
    try:
        message = service.users().messages().send(
            userId='me',
            body={'raw': encoded_message}
        ).execute()
        
        return f"Email sent successfully. Message ID: {message['id']}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

@mcp.tool()
def reply_to_email(email_id: str, body: str) -> str:
    """
    Reply to an existing email.
    
    Args:
        email_id: ID of the email to reply to
        body: Text content of the reply
    """
    service = get_gmail_service()
    
    try:
        # Get the original message to extract headers
        original = service.users().messages().get(userId='me', id=email_id).execute()
        
        # Get thread ID for maintaining the conversation
        thread_id = original.get('threadId', '')
        
        # Extract headers
        headers = original['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        # If subject doesn't start with Re:, add it
        if not subject.startswith('Re:'):
            subject = f"Re: {subject}"
            
        # Get the sender to use as recipient for the reply
        from_header = next((h['value'] for h in headers if h['name'] == 'From'), '')
        
        # Create reply message
        reply = MIMEText(body)
        reply['to'] = from_header
        reply['subject'] = subject
        reply['References'] = next((h['value'] for h in headers if h['name'] == 'Message-ID'), '')
        reply['In-Reply-To'] = next((h['value'] for h in headers if h['name'] == 'Message-ID'), '')
        
        # Set sender if specified in environment
        user_email = os.getenv('GMAIL_USER_EMAIL')
        if user_email:
            reply['from'] = user_email
        
        # Encode the message
        encoded_message = base64.urlsafe_b64encode(reply.as_bytes()).decode()
        
        # Send the reply
        message = service.users().messages().send(
            userId='me',
            body={
                'raw': encoded_message,
                'threadId': thread_id
            }
        ).execute()
        
        return f"Reply sent successfully. Message ID: {message['id']}"
    except Exception as e:
        return f"Failed to send reply: {str(e)}"

# Run the server when executed directly
if __name__ == "__main__":
    mcp.run(transport='stdio')
