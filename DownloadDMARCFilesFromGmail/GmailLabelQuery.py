class GmailLabelQuery:
    def __init__(self, service):
        self.service = service
        self.labels = None

    def __fetchLabels__(self):
        results = self.service.users().labels().list(userId="me").execute()
        self.labels = results.get('labels', [])

    def __getAllLabels__(self):
        if not self.labels:
            self.__fetchLabels__()

        return self.labels

    def labelIdFromName(self, name):
        return next(it['id'] for it in self.__getAllLabels__() if it['name'] == name)
