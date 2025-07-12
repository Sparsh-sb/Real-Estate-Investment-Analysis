import pandas as pd
import sqlite3
import os
import logging
import re

# Setup logging
os.makedirs("../logs", exist_ok=True)
logging.basicConfig(
    filename="../logs/build_property_summary.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

DB_PATH = "../real_estate.db"

DECODER_MAP = {
    'FACING': ('facing_direction', 'id', 'label'),
    'AGE': ('age', 'id', 'label'),
    'PROPERTY_TYPE__U': ('property_type', 'id', 'label'),
    'BATHROOM_NUM': ('bathroom_num', 'id', 'label'),
    'BEDROOM_NUM': ('bedroom_num', 'id', 'label'),
    'FLOOR_NUM': ('floor_num', 'id', 'label'),
    'TOTAL_FLOOR': ('total_floor', 'id', 'label'),
    'OWNTYPE': ('ownership_type', 'id', 'label'),
}

def load_table(table_name, conn):
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    logging.info(f"📥 Loaded table '{table_name}' with {df.shape[0]} rows and {df.shape[1]} columns.")
    return df

def decode_column(df, decode_df, key, value, column_to_decode):
    if column_to_decode not in df.columns:
        logging.warning(f"⚠️ Column '{column_to_decode}' not found in city dataset. Skipping.")
        return df

    # Pad column values to match decoder keys (e.g., 1 → '001')
    if column_to_decode == 'BEDROOM_NUM':
        df[column_to_decode] = df[column_to_decode].dropna().astype(int).astype(str).str.zfill(3)

    decode_map = dict(zip(decode_df[key], decode_df[value]))
    df[column_to_decode] = df[column_to_decode].map(decode_map)

    return df

def clean_price(price):
    try:
        if pd.isna(price) or "Price on Request" in price:
            return None
        price = price.split("-")[0].strip()
        if "Cr" in price:
            return float(re.sub(r"[^\d.]", "", price)) * 1e7
        elif "L" in price:
            return float(re.sub(r"[^\d.]", "", price)) * 1e5
        else:
            return float(re.sub(r"[^\d.]", "", price))
    except:
        return None

def clean_area(area):
    try:
        area = str(area).replace("sq.ft.", "").replace("sqft", "").strip()
        if "-" in area:
            parts = area.split("-")
            return (float(parts[0].strip()) + float(parts[1].strip())) / 2
        return float(area.replace(",", "").strip())
    except:
        return None

def process_city(city_name):
    conn = sqlite3.connect(DB_PATH)
    logging.info(f"\n🔍 Processing city: {city_name}")
    df = load_table(city_name, conn)

    # Decode
    for col, (decode_table, key_col, val_col) in DECODER_MAP.items():
        try:
            decode_df = load_table(decode_table, conn)
            df = decode_column(df, decode_df, key_col, val_col, col)
        except Exception as e:
            logging.warning(f"❌ Could not decode {col} using {decode_table}: {e}")
    logging.info(f"🔁 After decoding: {df.shape}")

    # Area column priority
    area_col = None
    for col in ["SUPERBUILTUP_SQFT", "AREA", "MAX_AREA_SQFT", "MIN_AREA_SQFT"]:
        if col in df.columns:
            area_col = col
            break

    if area_col:
        df["PRICE_CLEANED"] = df["PRICE"].apply(clean_price)
        df["AREA_CLEANED"] = df[area_col].apply(clean_area)
        df.dropna(subset=["PRICE_CLEANED", "AREA_CLEANED"], inplace=True)
        df = df[df["AREA_CLEANED"] != 0]

        df["PRICE_PER_SQFT"] = df["PRICE_CLEANED"] / df["AREA_CLEANED"]
        logging.info(f"🧮 Computed PRICE_PER_SQFT using '{area_col}'")
        logging.info(f"🧹 Dropped {df.shape[0]} rows after cleaning PRICE and AREA")
    else:
        logging.warning("⚠️ No valid area column found. Skipping PRICE_PER_SQFT calculation.")

    df.drop_duplicates(inplace=True)
    df.reset_index(drop=True, inplace=True)
    logging.info(f"📐 Final shape: {df.shape}")

    summary_table = f"{city_name}_summary"
    df.to_sql(summary_table, conn, if_exists="replace", index=False)
    logging.info(f"✅ Saved to DB table '{summary_table}' with {len(df)} rows.")

    output_path = f"../data/processed/{summary_table}.csv"
    df.to_csv(output_path, index=False)
    logging.info(f"📦 Exported to {output_path}")
    conn.close()

if __name__ == "__main__":
    for city in ["mumbai", "kolkata", "gurgaon_10k", "hyderabad"]:
        process_city(city)
