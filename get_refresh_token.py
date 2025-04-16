"""
Helper script to obtain a Gmail API refresh token.
"""
import os
from google_auth_oauthlib.flow import InstalledAppFlow

# Only requesting sending permissions
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    print("Gmail API Authentication Helper")
    print("===============================")
    print("This script will help you get a refresh token for the Gmail API.")
    print("Make sure you have already created a credentials.json file from the Google Cloud Console.")
    print("See the README.md for instructions on how to obtain the credentials.json file.")
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("\nError: credentials.json file not found!")
        print("Please follow the instructions in the README.md to create this file first.")
        return
    
    print("\nStarting authentication flow...")
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        SCOPES
    )
    
    creds = flow.run_local_server(port=0)
    print("\nAuthentication successful!")
    print("\n=== YOUR REFRESH TOKEN ===")
    print(creds.refresh_token)
    print("=========================")
    print("\nAdd this token to your .env file as GMAIL_REFRESH_TOKEN=<token>")

if __name__ == "__main__":
    main()
