import pandas as pd
import sqlite3
import os

# 1. Define Paths
raw_file = 'data-raw/R1-Palay_Corn-Production-2020-2025.csv'
cleaned_dir = 'data-cleaned'
db_path = os.path.join(cleaned_dir, 'production.db')

# Ensure the cleaned directory exists
if not os.path.exists(cleaned_dir):
    os.makedirs(cleaned_dir)

def clean_and_store():
    # 2. Load Data (Skip the first row which is a title, use ';' as delimiter based on your image)
    df = pd.read_csv(raw_file, skiprows=1, sep=';')

    # 3. "Unpivot" the data (Melt)
    # This turns your multiple columns (2020 Q1, 2020 Q2...) into rows
    id_vars = ['Ecosystem/Croptype', 'Geolocation']
    value_vars = [col for col in df.columns if col not in id_vars]
    
    df_long = pd.melt(
        df, 
        id_vars=id_vars, 
        value_vars=value_vars, 
        var_name='Period', 
        value_name='Volume_Metric_Tons'
    )

    # 4. Clean up the 'Period' column (Optional: separate Year and Quarter)
    # Example: "2020 Quarter 1" -> Year: 2020, Quarter: Q1
    df_long['Year'] = df_long['Period'].str.extract(r'(\d{4})')
    df_long['Quarter_Type'] = df_long['Period'].str.replace(r'\d{4}\s+', '', regex=True)

    # 5. Connect to SQLite and Save
    conn = sqlite3.connect(db_path)
    
    # This creates the table 'crop_production' inside the .db file
    df_long.to_sql('crop_production', conn, if_exists='replace', index=False)
    
    conn.close()
    print(f"Success! Database created at: {db_path}")

if __name__ == "__main__":
    clean_and_store()