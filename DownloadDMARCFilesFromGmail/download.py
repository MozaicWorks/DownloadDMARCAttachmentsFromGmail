from GmailAuth import GmailAuth
from GmailLabelQuery import GmailLabelQuery
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description='Download DMARC attachments from your Gmail account. The emails are found based on a label, and once the download is succesfull the processed label is applied. First you need to setup a Google Cloud Console app that allows access to Gmail API. Visit https://console.cloud.google.com to set it up, copy the authentication file to the secrets folder, and rename it to "client_id.json".'
    )
    parser.add_argument(
        '--labelName',
        type=str,
        help='The Gmail label assigned to DMARC emails. Default is "DMARC"',
        default="DMARC",
    )
    parser.add_argument(
        '--processedLabelName',
        type=str,
        help='The Gmail label that will be assigned to processed DMARC emails. Default is "PROCESSED_DMARC"',
        default="PROCESSED_DMARC",
    )

    args = parser.parse_args()

    labelName = args.labelName
    processedLabelName = args.processedLabelName
    try:
        service = authenticate()
    except Exception as e:
        print(e)
        sys.exit(
            "ERROR: Authentication failed. Have you enabled access to Gmail API? Check https://github.com/MozaicWorks/DownloadDMARCAttachmentsFromGmail#how-to-use for instructions"
        )

    labelQuery = GmailLabelQuery(service)
    labelId = labelQuery.labelIdFromName(labelName)
    replaceWithLabelId = labelQuery.labelIdFromName(processedLabelName)

    downloadAttachments(service, labelId, replaceWithLabelId, "out/")


def downloadAttachments(service, labelId, replaceWithLabelId, downloadPath):
    messages = messagesWithLabel(service, labelId)["messages"]
    print("Found {messageCount} messages".format(messageCount=len(messages)))
    createDownloadPath(downloadPath)

    for message in messages:
        try:
            processMessage(service, message["id"], labelId, replaceWithLabelId)
        except Exception:
            print("Error at message {message}".format(message=message))


def processMessage(service, messageId, labelId, replaceWithLabelId):
    downloadAttachment(service, messageId, "out/")
    markMessageAsProcessed(service, messageId, labelId, replaceWithLabelId)


def createDownloadPath(downloadPath):
    if not os.path.exists(downloadPath):
        os.makedirs(downloadPath)


def authenticate():
    scopes = ['https://www.googleapis.com/auth/gmail.modify']
    return GmailAuth(scopes).authenticateWithClientAccount()


def markMessageAsProcessed(service, messageId, labelId, replaceWithLabelId):
    modifyMessageRequest = {
        'removeLabelIds': [labelId],
        'addLabelIds': [replaceWithLabelId],
    }
    service.users().messages().modify(
        userId="me", id=messageId, body=modifyMessageRequest
    ).execute()


def labelIdFromName(service, name):
    results = service.users().labels().list(userId="me").execute()
    labels = results.get('labels', [])
    return next(it['id'] for it in labels if it['name'] == name)


def messagesWithLabel(service, labelId):
    MAX_ALLOWED_MESSAGES_COUNT = 500
    return (
        service.users()
        .messages()
        .list(userId="me", maxResults=MAX_ALLOWED_MESSAGES_COUNT, labelIds=[labelId])
        .execute()
    )


def downloadAttachment(service, messageId, downloadPath):
    import base64

    message = service.users().messages().get(userId="me", id=messageId).execute()
    if message["payload"]["filename"]:
        fileName = message["payload"]["filename"]
        print("Processing file {fileName}".format(fileName=fileName))
        attachmentId = message["payload"]["body"]["attachmentId"]
    else:
        part = next(
            it
            for it in message["payload"]["parts"]
            if it["mimeType"] == "application/octet-stream"
            or it["mimeType"] == "application/gzip"
        )
        fileName = part["filename"]
        print("Processing file {fileName}".format(fileName=fileName))
        attachmentId = part["body"]["attachmentId"]

    attachment = (
        service.users()
        .messages()
        .attachments()
        .get(userId="me", messageId=messageId, id=attachmentId)
        .execute()
    )
    data = attachment['data']

    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))

    filePath = os.path.join(downloadPath, fileName)
    with open(filePath, 'wb') as f:
        f.write(file_data)

    print("File {fileName} written".format(fileName=fileName))


if __name__ == "__main__":
    main()
