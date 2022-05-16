# Jose M. Aguilar 
# Setups the credentials to be able to use the API
# IMPORTANT: You will need a credentials.json file made by Google Cloud Console

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


def api_setup():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # If you get an error saying the token is expired just delete it and run 
    # the program again.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) # The credentials.json file is the key that was made in the Google Cloud Console
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Build the Gmail API service
        service = build('gmail', 'v1', credentials=creds)

    except HttpError as error:
        # Errors from gmail API.
        print(f'An error occurred: {error}')
    
    return service