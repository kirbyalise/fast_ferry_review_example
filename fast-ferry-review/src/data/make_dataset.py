import pandas as pd
import os
from pathlib import Path

def load_data():
    crew_change_over = pd.read_csv('src/data/raw/crew_change_over.csv')
    shift_change = pd.read_csv('src/data/raw/shift_change.csv')
    
    return crew_change_over, shift_change

if __name__ == '__main__':
    print("Loading raw data sets.")
    crew_data, shift_data = load_data()
    print(f"Crew data loaded with {len(crew_data)} rows.")
    print(f"Shift data loaded with {len(shift_data)} rows.")  


