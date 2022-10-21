from .GmailAuth import *

def main():
    pass

def authenticate():
    scopes = ['https://www.googleapis.com/auth/gmail.readonly']
    return GmailAuth(scopes).authenticateWithClientAccount()

 

if(__name__ == "__main__"):
    main()
