# Download DMARC Attachments From Gmail

## Description

A tool to download DMARC from Gmail email attachments. Consider it under development, so use with care. Feedback and PRs are welcome!

## How To Use

First, you need to give the tool access to your Gmail account through the API. Here's how to do it for a workspace account:

* Access [https://console.cloud.google.com/](https://console.cloud.google.com/)
* Create a new project, for example named "DownloadDMARCAttachments"
* Select the newly created project
* Enable the Gmail API
  * Navigate to the [API Console](https://console.developers.google.com/)
  * Select on **ENABLE APIS AND SERVICES**
  * Search for **gmail**
  * Select **Gmail API**
  * Select **Enable**
* Configure the **OAuth consent**
  * Select **OAuth consent screen** from the left navigation pane
  * Go throught the wizard to create an App
  * Use in scopes 'https://www.googleapis.com/auth/gmail.modify'
* Configure the **Credentials**
  * Select **Credentials** from the left navigation pane
  * Select **CREATE CREDENTIALS** and select **OAuth Client ID**
  * For **Application type** select **Desktop app**
  * For **Name** fill in "DownloadDMARCAttachments"
  * Select **Create**
  * Download the JSON file
* Create a `secrets` folder, copy the client json file into it, and rename it to `client_id.json`

Second, you need to ensure that all the DMARC messages in your Gmail inbox have a label. By default, the label is "DMARC".

Third, create a label under which the messages will be posted after a successful download of the attachment. By default, the tool uses "PROCESSED_DMARC".

You are now ready to run it. Just pass in the label name and the processed label name, if different from the defaults. The tool will download the attachments for messages found under the DMARC label into an `out` folder and replace the DMARC label with the processed label. This allows you to double check the results, and do whatever you want with the processed messages.

## Renewing OAuth Client ID

When renewing the OAuth Client ID, download the OAuth client JSON file again.

Move the file to `./secrets/client_id.json`.

Delete the file `./secrets/token.pickle`.

## Known Issues

We're still figuring out the different ways the attachment id is found in Gmail messages, so processing fails for some messages.

## Limitations

Due to limitations in the Gmail API, the tool processes max. 500 messages at once. If you have more than 500 DMARC messages, just run it again until you process all the files.

## Generating a report

If you're looking for a simple tool to generate a report from the downloaded attachments, check out the companion tool [DMARC Reporting](https://github.com/MozaicWorks/DMARCReporting).

## Development setup

* Make sure you have python 3.10
* Install [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

With default arguments, i.e. `--labelName DMARC --processedLabelName PROCESSED_DMARC`

```bash
make install
make run
```

To pass arguments:

```bash
make run args="--labelName dmarc --processedLabelName processed-dmarc"
```

## Development Notes

This tool was started by [Alex Bolboaca](https://twitter.com/alexboly) to automate the DMARC processing flow that he uses.
