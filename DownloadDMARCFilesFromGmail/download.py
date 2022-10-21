from .GmailAuth import *

def main():
    pass

def authenticate():
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    return GmailAuth(scopes).authenticateWithClientAccount()

def labelIdFromName(service, name):
        results = service.users().labels().list(userId="me").execute()
        labels = results.get('labels', [])
        return next(it['id'] for it in labels if it['name']==name)
 
 

if(__name__ == "__main__"):
    main()
