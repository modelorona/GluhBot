import googleapiclient.discovery
import asyncio
from google.oauth2 import service_account
from os import getenv, path, listdir


class GoogleDriveFolderDownloader():
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/drive']
        service_account_file = 'credentials.json'
        credentials = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=scopes)
        self.audio = 'test_audio'
        self.drive = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
        self.folder_id = getenv('DRIVE_FOLDER_ID')

    def audio_folder_exists(self):
        return path.exists('test_audio') 

    def download_audio(self):
        if self.audio_folder_exists:
            print('audio folder already exists, will not download audio files')
        else:
            print('audio folder does not exist, starting file downloads')
            self.download_all_audio()

    def download_all_audio(self):
        files = self.drive.files().list(q="'{}' in parents".format(self.folder_id)).execute().get('files', [])
        if files is []:
            print('google drive api returned empty folder, check api or permissions')
        else:
            print('google drive files found, downloading')
