# Gmail Sender MCP Server

A Model Context Protocol (MCP) server that enables Claude and other AI assistants to send emails via Gmail API. This focused version only provides email sending capabilities.

## Overview

This project creates an MCP server that allows AI assistants to:
- Send new emails
- Reply to existing emails

It's designed to be lightweight and easy to set up, using the Gmail API for email operations.

## Prerequisites

- Python 3.8 or higher
- A Google Cloud account with Gmail API enabled
- Docker (optional, for containerized deployment)

## Setup Instructions

### 1. Create a Google Cloud Project and Enable the Gmail API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. In the sidebar, navigate to "APIs & Services" > "Library"
4. Search for "Gmail API" and enable it
5. Go to "APIs & Services" > "Credentials"
6. Click "Create Credentials" and select "OAuth client ID"
7. For application type, choose "Desktop app"
8. Name your OAuth client
9. Click "Create"
10. Download the credentials JSON file

### 2. Prepare Your Environment

Clone this repository:

```bash
git clone https://github.com/abhishekloiwal/gmail-sender-mcp.git
cd gmail-sender-mcp
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set Up Your Credentials

1. Rename the downloaded credentials file to `credentials.json` and place it in the project root directory
2. Run the helper script to get a refresh token:

```bash
python get_refresh_token.py
```

3. Follow the authentication flow in your browser
4. Copy the refresh token that appears in the terminal
5. Create a `.env` file based on the example:

```bash
cp .env.example .env
```

6. Edit the `.env` file and fill in your credentials:

```
GMAIL_CLIENT_ID=your-client-id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your-client-secret
GMAIL_REFRESH_TOKEN=your-refresh-token
GMAIL_USER_EMAIL=your-email@gmail.com
```

### 4. Run the MCP Server

```bash
python gmail_sender.py
```

The server will start and listen for connections.

## Docker Deployment

You can also run the server in a Docker container:

### Build and Run with Docker

```bash
docker build -t gmail-sender-mcp .
docker run -d --name gmail-sender-mcp --env-file .env gmail-sender-mcp
```

### Or Use Docker Compose

```bash
docker-compose up -d
```

## Using with Claude or other AI Assistants

To use this MCP server with an AI assistant, you'll need to:

1. Run the MCP server
2. Connect your AI assistant to the MCP server (specific steps depend on your AI platform)

The MCP server provides the following tools:

### `send_email` Tool

Sends a new email.

Parameters:
- `to`: Recipient email address
- `subject`: Email subject line
- `body`: Email body content (HTML formatting supported)

### `reply_to_email` Tool

Replies to an existing email.

Parameters:
- `email_id`: ID of the email to reply to
- `body`: Reply content (HTML formatting supported)

## Security Considerations

- Keep your `.env` file secure and never commit it to version control
- The refresh token grants access to send emails from your account, so treat it like a password
- Consider using a dedicated Google account for this integration if you're concerned about security

## Troubleshooting

Common issues:

- **Authentication errors**: Make sure your credentials in the `.env` file are correct
- **Permission errors**: Verify that you've enabled the Gmail API in your Google Cloud project
- **Token expired**: If your refresh token stops working, generate a new one using the helper script

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.