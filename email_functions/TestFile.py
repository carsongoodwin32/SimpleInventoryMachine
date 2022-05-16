# Jose M. Aguilar 
# This just tests the function that was made in #EmailFunc.py

import EmailFunc

# Sends three different messages. 
for x in range (3): # Ends at 2
    EmailFunc.makeAndSendMessage('[INSERT_SENDER_EMAIL]', '[INSERT_RECIPIENT_EMAIL)', '[INSERT_TICKET_NUMBER]', x, \
    '[INSERT_LAPTOP_NAME]\n[INSERT_LAPTOP_NAME]\n[INSERT_LAPTOP_NAME]\n' + 'Message option ' + str(x))