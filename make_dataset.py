import pandas as pd
import os
from pathlib import Path
# Removed pyodbc import as it's no longer needed
# from config import user_name_odp, password_odp

# Removed get_crew_data and get_shift_data functions

def load_data():
    crew_change_over = pd.read_csv('src/data/raw/crew_change_over.csv')
    shift_change = pd.read_csv('src/data/raw/shift_change.csv')
    
    return crew_change_over, shift_change

if __name__ == '__main__':
    print("Loading raw data sets.")
    crew_data, shift_data = load_data()
    print(f"Crew data loaded with {len(crew_data)} rows.")
    print(f"Shift data loaded with {len(shift_data)} rows.")  


