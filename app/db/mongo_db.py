from pymongo import MongoClient
import pandas as pd
from app.repositories.attacks_repo import insert_many
from app.services.normalize_service import normalize_second_csv, normalize
from app.services.read_files_service import get_file_path
from app.settings.config import DB_URL


my_client = MongoClient(DB_URL)
mydb = my_client["terror_attacks_db"]
attacks_col = mydb["attacks"]


def initialize_mongo(uri: str, database_name: str, collection_name: str):
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]
    return collection


def init_db():
    col = initialize_mongo(DB_URL, "terror_attacks_db", "attacks")
    if col.count_documents({}) == 0:
        print("Database is empty. Initializing...")
        col.drop()
        csv1_file_path = get_file_path('RAND_Database_of_Worldwide_Terrorism_Incidents.csv')
        data_frame = pd.read_csv(csv1_file_path, encoding='latin-1')
        data = normalize_second_csv(data_frame)
        insert_many(col, data.to_dict('records'))
        print('csv1 inserted')
        json_file_path = get_file_path('globalterrorismdb_0718dist.json')
        data_frame = pd.read_json(json_file_path)
        df = normalize(data_frame)
        insert_many(col, df.to_dict('records'))
        print('csv2 inserted')
    else:
        print("Database is already populated. Skipping initialization.")