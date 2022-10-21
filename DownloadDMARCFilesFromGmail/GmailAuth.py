from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

import os
import pickle

class GmailAuth:

    def __init__(self, scopes, clientIdFileName="secrets/client_id.json", tokenFileName="secrets/token.pickle", serviceAccountIdFileName="secrets/service_id.json"):
        self.clientIdFileName = clientIdFileName
        self.scopes = scopes
        self.tokenFileName = tokenFileName
        self.serviceAccountIdFileName=serviceAccountIdFileName

    def authenticateWithClientAccount(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.tokenFileName):
            with open(self.tokenFileName, 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.clientIdFileName, self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.tokenFileName, 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def authenticateWithServiceAccount(self, fromEmail):
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_file(self.serviceAccountIdFileName, scopes=self.scopes)
        return build('gmail', 'v1', credentials=creds.with_subject(fromEmail))
