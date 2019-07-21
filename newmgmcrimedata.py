# Copyright 2019 ZALME LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function
import pickle
import base64
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    
    # Debug Labels
    #response = service.users().labels().list(userId='me').execute()
    #labels = response['labels']
    #for label in labels:
    #    print ('Label id: %s - Label name: %s' % (label['id'], label['name']))
   
    results = service.users().messages().list(userId='me',labelIds=['Label_984599473385438091']).execute()

    messages = results.get('messages', [])
    for message in messages:
        #msg = service.users().messages().get(userId='me', id=message['id'] ,format='raw').execute()
        msg = service.users().messages().get(userId='me', id=message['id'] ,format='full' ).execute()
        payld = msg['payload']
        headr = payld['headers']
       
        #body = base64.urlsafe_b64decode(msg['raw'].encode('ASCII'))
        #body = str(msg['payload'])
        #if ( "CrimeMapping.com" in str(body) ):
        for one in headr:
            if one['name'] == 'Subject':
                 
                msg_subject = one['value']
                print(msg_subject)
                if ( "CrimeMapping.com" in str(msg_subject) ):
                    #print (str(msg_subject) + "\n\n\nXXXXXXXXXXXXXXXXXXXXX\n\n\n") 
                    payldmssg_parts = payld['body']
                    body = base64.urlsafe_b64decode(payldmssg_parts['data'].encode('ASCII'))
                    p1 = str(body).replace("\\r\\n","~").replace("\\xe2\\x80\\x94","")
                    #print (str(p1) + "\n\n\nXXXXXXXXXXXXXXXXXXXXX\n\n\n") 
                    out1 = p1.replace("~","\n")
                    print(out1)     #part_one  = mssg_parts[0] # fetching first element of the part 
                         #part_body = base64.urlsafe_b64decode(part_one['body'].encode('ASCII'))
                         #print (str(part_body) + "\n\n\nXXXXXXXXXXXXXXXXXXXXX\n\n\n") 


           #print (str(body) + "\n\n\nXXXXXXXXXXXXXXXXXXXXX\n\n\n") 


if __name__ == '__main__':
    main()
# [END gmail_quickstart]
