import googleapiclient.discovery
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from io import BytesIO
from os import getenv, path, mkdir
from set_up_logging import get_logger


class GoogleDriveFolderDownloader():
    def __init__(self):
        scopes = ['https://www.googleapis.com/auth/drive']
        # todo: need to convert this to env friendly way for build
        service_account_file = 'credentials.json'
        credentials = service_account.Credentials.from_service_account_file(
                service_account_file, scopes=scopes)
        self.audio = 'audio'
        self.drive = googleapiclient.discovery.build('drive', 'v3', credentials=credentials)
        self.folder_id = getenv('DRIVE_FOLDER_ID')

    def audio_folder_exists(self) -> bool:
        return path.exists(self.audio)

    def download_audio(self):
        if self.audio_folder_exists():
            get_logger().info('audio folder already exists, will not download audio files')
        else:
            get_logger().info('audio folder does not exist, starting file downloads')
            try:
                mkdir(self.audio)
            except OSError as e:
                get_logger().error(e)
                return
            self.download_all_audio()

    def download_all_audio(self):
        files = self.drive.files().list(q="'{}' in parents".format(self.folder_id)).execute().get('files', [])
        if files is []:
            get_logger().info('google drive api returned empty folder, check api or permissions')
        else:
            get_logger().info('google drive files found, downloading')
            # file_n_ids = [(file.get('id', None), file.get('name', None)) for file in files]
            for file in files:
                if file.get('id', None) is None or file.get('name', None) is None: continue  # just in case
                get_logger().info('downloading audio file: ' + file.get('name'))
                req = self.drive.files().get_media(fileId=file.get('id'))
                fh = BytesIO()
                downloader = MediaIoBaseDownload(fh, req)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
                with open(self.audio + '/' + file.get('name'), 'wb') as audio_file:
                    audio_file.write(fh.getbuffer())
                    get_logger().info('downloaded audio file: ' + file.get('name'))
            
