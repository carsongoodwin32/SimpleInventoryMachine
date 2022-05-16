# Jose M. Aguilar 
# These functions are used to build the email that will be sent out.

import APISetup
import base64

# Gmail API utils
from googleapiclient.errors import HttpError
# for dealing with attachement MIME types
from email.mime.text import MIMEText

from googleapiclient.errors import HttpError

# Sends the message using the Google Gmail API Service
def __sendMessage(service, message):
    user_id = "me"

    try:
        message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
        print(f'*** Message Sent ***\nMessage ID: {message}')
        return message
    except HttpError as error:
        print(f'An error occurred: {error}') 

# This function creates the email using the user information.
# The user can choose to send an email saying the item was checked in or out. 
def __makeMessage(sender, to, subject, messageText):

    message = MIMEText(messageText)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    
    rawMessage = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    return rawMessage

# sender = string, to = string, messageOption = int, item = string
# If you have multiple items format the string with newlines (\n) example: (computer1\computer2\ncomputer3)
def makeAndSendMessage(sender, to, subject, messageOption, item):
    messageText = 'Hello,\nI\'m just a bot. If you have questions feel free to reply.' # Can probably leave this as the defualt

    if messageOption == 0:
        messageText = 'Hello,\nYou checked out: \n' + item + '\nIf you have questions or concerns feel free to reply.\
        \n\nBest Regards,\nSAtech Inventory Bot'
    elif messageOption == 1:
        messageText = 'Hello,\nYou checked in: \n' + item + '\nIf you have questions or concerns feel free to reply.\
        \n\n\nBest Regards,\nSAtech Inventory Bot' 

    theMessage = __makeMessage(sender, to, subject, messageText)
    __sendMessage(APISetup.api_setup(), theMessage)