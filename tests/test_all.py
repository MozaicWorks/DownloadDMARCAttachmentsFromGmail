import unittest
from DownloadDMARCFilesFromGmail.download import *

class AllTests(unittest.TestCase):

    def test_authenticate(self):
        service = authenticate()
        labelId = labelIdFromName(service, "DMARC")
       
        message = service.users().messages().list(userId="me", maxResults=1, labelIds=[labelId]).execute()
        print(message)

if(__name__ == "__main__"):
    unittest.main()
