# Gmail OAuth Credentials Directory

This directory is intended to store your local Google OAuth 2.0 Client Credentials and authentication tokens.

> ⚠️ **SECURITY NOTICE**: Never commit your `credentials.json` or `token.json` files to Git or any public repository. They are automatically ignored by `.gitignore`.

## How to setup your `credentials.json`

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (e.g., `Smart Email Organizer`).
3. Enable the **Gmail API**:
   - Go to **APIs & Services > Library**.
   - Search for **Gmail API** and click **Enable**.
4. Configure OAuth Consent Screen:
   - Go to **APIs & Services > OAuth consent screen**.
   - Select **External** (or Internal for Workspace users).
   - Fill in mandatory fields (App name, support email, developer email).
   - Under **Scopes**, add `https://www.googleapis.com/auth/gmail.modify`.
   - Under **Test users**, add your own Gmail address.
5. Create OAuth 2.0 Client Credentials:
   - Go to **APIs & Services > Credentials**.
   - Click **Create Credentials > OAuth client ID**.
   - Select Application type: **Desktop app**.
   - Name it `Smart Email Organizer Desktop Client`.
   - Click **Create**, then click **Download JSON**.
6. Move the downloaded JSON file into this folder and rename it to `credentials.json`:
   ```
   smart-email-organizer-mcp/credentials/credentials.json
   ```

When you first run `python server.py` or execute an MCP tool, a browser window will open asking you to authorize the app. Once authorized, a `token.json` file will be generated in this directory to maintain authentication across sessions.
