import unittest
from DownloadDMARCFilesFromGmail.download import authenticate

class AllTests(unittest.TestCase):

    def test_authenticate(self):
        service = authenticate()
        message = service.users().messages().list(userId="me", maxResults=1).execute()

if(__name__ == "__main__"):
    unittest.main()
