import pymongo
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1U_XhwM7U98lLApk-vAMQjFnTYh00xsAVjENUM13dIpU' 
class MongoDBPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.creds = None
        self.service = None
        self.authenticate_google_sheets()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'scrapy_db')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def authenticate_google_sheets(self):
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not self.creds or not self.creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            self.creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        self.service = build('sheets', 'v4', credentials=self.creds)

    def process_item(self, item, spider):
        # Save to MongoDB
        collection_name = spider.name
        self.db[collection_name].insert_one(dict(item))

        # Prepare data for Google Sheets
        values = [[
            item.get('titles', ''),
            item.get('prices', ''),
            item.get('ratings', ''),
            item.get('availability', ''),
            item.get('links', '')
        ]]
        body = {'values': values}

        # Append row to Google Sheet
        self.service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A1',  # Adjust if your sheet name is different
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()

        return item