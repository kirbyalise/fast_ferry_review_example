import pandas as pd
import os
from pathlib import Path
import pyodbc
from config import user_name_odp, password_odp

def get_crew_data() -> pd.DataFrame:
    """Query the ODS database and return raw data as a data frame. Save output as .csv file."""
    # Fix: Update the SQL file path to use the correct directory structure
    sql_file_path = Path().resolve().joinpath('./fast_ferry_review_amrun/src/data/sql/crew_change_over_amrun.sql')
    with open(sql_file_path) as f:
        sql_statement = f.read()
    # Connection string.
    conn_str = (
        "Driver={SQL Server};"
        "Server=odp-rtapacops-wei-ods.corp.riotinto.org;"
        "Database=ODS_WENCO;"
        f"uid={user_name_odp};"
        f"pwd={password_odp};"
    )
    print(conn_str)
    # Connect to ODS database and execute SQL statement to create a data frame.
    conn = pyodbc.connect(conn_str)
    print('Querying ODS database.')
    df = pd.read_sql(
        sql_statement,
        con=conn
    )
    print('Raw data frame created with {} rows.'.format(len(df)))

    # Create the data directory if it doesn't exist
    raw_data_dir = Path().resolve().joinpath('fast_ferry_review_amrun/src/data/raw')
    if not raw_data_dir.exists():
        os.makedirs(raw_data_dir)
    
    # Save to CSV with proper filename
    output_path = raw_data_dir / 'crew_change_over_amrun.csv'
    df.to_csv(output_path, index=False)
    print(f'Data saved to {output_path}')

    return df

if __name__ == '__main__':
    print("Creating raw data sets.")
    get_crew_data()  



def get_shift_data() -> pd.DataFrame:
    """Query the ODS database and return raw data as a data frame. Save output as .csv file."""
    # Fix: Update the SQL file path to use the correct directory structure
    sql_file_path = Path().resolve().joinpath('./fast_ferry_review_amrun/src/data/sql/shift_change_amrun.sql')
    with open(sql_file_path) as f:
        sql_statement = f.read()
    # Connection string.
    conn_str = (
        "Driver={SQL Server};"
        "Server=odp-rtapacops-wei-ods.corp.riotinto.org;"
        "Database=ODS_WENCO;"
        f"uid={user_name_odp};"
        f"pwd={password_odp};"
    )
    print(conn_str)
    # Connect to ODS database and execute SQL statement to create a data frame.
    conn = pyodbc.connect(conn_str)
    print('Querying ODS database.')
    df = pd.read_sql(
        sql_statement,
        con=conn
    )
    print('Raw data frame created with {} rows.'.format(len(df)))

    # Create the data directory if it doesn't exist
    raw_data_dir = Path().resolve().joinpath('fast_ferry_review_amrun/src/data/raw')
    if not raw_data_dir.exists():
        os.makedirs(raw_data_dir)
    
    # Save to CSV with proper filename
    output_path = raw_data_dir / 'shift_change_amrun.csv'
    df.to_csv(output_path, index=False)
    print(f'Data saved to {output_path}')

    return df

if __name__ == '__main__':
    print("Creating raw data sets.")
    get_shift_data()  
