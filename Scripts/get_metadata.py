import sqlite3
import pandas as pd
from sqlite3 import Error

def get_metadata(privilege = 0, ensemble = "", db_file = "/srv/scmdb_py/ensemble_data_config.db",\
                 postfix = "metadata_example.csv"):

    datasets = ensemble.split("_")
    if len(datasets) > 1:
        datasets = str(tuple(datasets))
    else:
        datasets = "('"+ensemble+"')"

    query = "SELECT * FROM dataset_config where Dataset in " + datasets + ";"
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    cur = conn.cursor()
    cur.execute(query)

    rows = cur.fetchall()
    df = pd.DataFrame()

    for r in rows:
        if privilege or (r[1] == 1):
            meta_path = r[5] + postfix
            print("Extracting data for: " + meta_path)
            try:
                temp = pd.read_csv(meta_path)
                df = df.append(temp)
            except:
                print("File '" + meta_path + "' not found.")

    if len(df) > 0:
        df = df.reset_index()
        return df.to_json()
    else:
        return False