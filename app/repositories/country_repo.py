import pandas as pd
from app.db.mongo_db import initialize_mongo
from app.repositories.attacks_repo import insert_many
from app.services.geolocation_service import get_country_coordinates
from app.services.read_files_service import get_file_path
from app.settings.config import API_KEY, DB_URL


def merge_countries(df1, df2, on, how):
    merged_df = pd.merge(df1, df2, how=how, on=on)
    print('Columns merged successfully')
    return merged_df


def change_column_name(df, old_name, new_name):
    df.rename(columns={old_name: new_name}, inplace=True)
    print('Column renamed successfully')
    return df


def convert_to_df(np_array, columns: list[str]):
    df = pd.DataFrame(np_array, columns=columns)
    print('df Converted successfully')
    return df





if __name__ == '__main__':
    csv1_file_path = get_file_path('RAND_Database_of_Worldwide_Terrorism_Incidents.csv')
    data_frame1 = pd.read_csv(csv1_file_path, encoding='latin-1')

    json_file_path = get_file_path('globalterrorismdb_0718dist.json')
    data_frame2 = pd.read_json(json_file_path)
    change_column_name(data_frame2, 'country_txt', 'Country')

    countries1 = data_frame1['Country'].unique()
    countries2 = data_frame2['Country'].unique()

    converted1 = convert_to_df(countries1, ['Country'])
    converted2 = convert_to_df(countries2, ['Country'])

    merged = merge_countries(converted1, converted2,['Country'], 'outer')

    merged['location'] = merged['Country'].apply(
        lambda country: get_country_coordinates(country, API_KEY)
    )

    print(merged.to_dict('records'))

    col = initialize_mongo(DB_URL, "terror_attacks_db", "countries")

    insert_many(col, merged.to_dict('records'))
    print('Data inserted successfully')


