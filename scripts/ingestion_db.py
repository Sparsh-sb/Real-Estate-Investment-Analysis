import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

# Setup logging
os.makedirs("../logs", exist_ok=True)
logging.basicConfig(
    filename="../logs/ingestion_db.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# Connect to SQLite
engine = create_engine("sqlite:///../real_estate.db")

def ingest_db(df, table_name):
    """Ingests a DataFrame into SQLite."""
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    logging.info(f"✅ Ingested {len(df)} rows into table '{table_name}'")

def load_city_data():
    """Ingests city-level CSVs into the database."""
    raw_path = "../data/raw"
    for file in os.listdir(raw_path):
        if file.endswith(".csv") and file != "README.csv":  # ignore readme or temp files
            file_path = os.path.join(raw_path, file)
            table_name = file[:-4].lower().replace(" ", "_")
            try:
                df = pd.read_csv(file_path)
                ingest_db(df, table_name)
            except Exception as e:
                logging.error(f"❌ Failed to ingest {file}: {e}")

def load_facets():
    """Ingests each file in the facets folder as its own table."""
    facets_path = "../data/raw/facets"
    if not os.path.exists(facets_path):
        logging.warning("⚠️ Facets folder not found.")
        return
    
    for file in os.listdir(facets_path):
        if file.endswith(".csv"):
            facet_path = os.path.join(facets_path, file)
            table_name = os.path.splitext(file)[0].lower().replace(" ", "_")
            try:
                df = pd.read_csv(facet_path)
                ingest_db(df, table_name)
            except Exception as e:
                logging.error(f"❌ Failed to ingest facet {file}: {e}")

def main():
    start = time.time()
    logging.info("🚀 Starting Ingestion Process")
    load_city_data()
    load_facets()
    duration = round((time.time() - start) / 60, 2)
    logging.info(f"✅ Ingestion complete in {duration} minutes.")

if __name__ == "__main__":
    main()