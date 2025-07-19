import pandas as pd
import os

cities = ['mumbai', 'kolkata', 'hyderabad', 'gurgaon']
folder = os.path.join("data", "processed")

output_path = os.path.join("exports", "real_estate_cleaned_data.xlsx")
os.makedirs("exports", exist_ok=True)

with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
    for city in cities:
        csv_path = os.path.join(folder, f"{city}_summary_cleaned.csv")
        df = pd.read_csv(csv_path)
        df.to_excel(writer, sheet_name=city.capitalize(), index=False)

print("Excel file exported successfully:", output_path)