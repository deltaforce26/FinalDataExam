import pandas as pd


def normalize(df):
    df = df.drop_duplicates()

    df.fillna({'nkill': 0, 'nwound': 0, 'city': 'Unknown', 'nperps': 0}, inplace=True)

    df['fatality_score'] = (df["nkill"] * 2) + (df["nwound"])

    df.rename(columns={"iyear": "year",
                       "imonth": "month", "iday": "day",
                       "targtype1_txt": "target_type", "attacktype1_txt": "attack_type",
                       'gname': 'terror_group', 'country_txt': 'country', 'summary': 'description',
                       'nkill': 'fatalities', 'nwound': 'injuries', 'weaptype1_txt' : 'weapon_type'}, inplace=True)

    mask = (df['month'] == 0) | (df['day'] == 0) | (df['city'] == 'Unknown')
    df = df[~mask]

    df['date'] = pd.to_datetime(dict(year=df.year, month=df.month, day=df.day))
    print("csv1 has been normalized")
    return df


def normalize_second_csv(df):
    df = df.drop_duplicates()
    df.loc[:, 'Date']  = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')
    df.loc[:, 'Date']  = df['Date'].apply(lambda x: x.replace(year=1900 + (x.year - 2000)) if x.year > 2024 else x)
    df = df.fillna({'City': 'Unknown', 'Perpetrator': 'Unknown', 'Weapon': 'Unknown', 'Description': 'Unknown'})
    df.rename(columns={"City": "city", "Country": "country", 'Description': 'description',
                       'Injuries': 'injuries', 'Fatalities': 'fatalities', 'Weapon': 'weapon_type',
                       'Perpetrator': 'terror_group', 'Date': 'date'}, inplace=True)
    df['fatality_score'] = (df["fatalities"] * 2) + (df["injuries"])
    print("csv2 has been normalized")
    return df


