import pandas as pd
import json
import csv

# Cleaning and Arranging Data Layer

# Load data
df = pd.read_csv("universities.csv")

# Clean 'Founded' column: extract 4-digit year from string
df["Founded"] = df["Founded"].astype(str).str.extract(r"(\d{4})")
df["Founded"] = pd.to_numeric(df["Founded"], errors='coerce').fillna(0).astype(int)

# Clean 'Enrollment' column: extract numbers, remove commas, convert to int
df["Enrollment"] = df["Enrollment"].astype(str).str.extract(r"(\d{1,3}(?:,\d{3})*)")
df["Enrollment"] = df["Enrollment"].str.replace(',', '', regex=False)
df["Enrollment"] = pd.to_numeric(df["Enrollment"], errors='coerce').fillna(0).astype(int)

# Split 'Location' into 'City' and 'Country'
df[["City", "Country"]] = df["Location"].str.split(",", n=1, expand=True)

# Clean and fill missing 'Country' with 'City' to avoid nulls
df["Country"] = df["Country"].fillna(df["City"]).str.strip()
df["City"] = df["City"].str.strip()

# Drop original 'Location' column
df = df.drop(columns=["Location"])

# Reorder columns: insert 'City' and 'Country' after column index 2
df.insert(2, "City", df.pop("City"))
df.insert(3, "Country", df.pop("Country"))

# Export cleaned data
df.to_csv("universities-clean.csv", index=False)

# Transformation layer
df = pd.read_csv("universities-clean.csv")

# Create dim_institution
dim_institution = df[['Institution', 'Affiliation', 'AttendanceMode', 'Founded', 'Link']].drop_duplicates().reset_index(drop=True)
dim_institution['institution_id'] = dim_institution.index + 1

# Create dim_location
dim_location = df[['City', 'Country', 'Continent']].drop_duplicates().reset_index(drop=True)
dim_location['location_id'] = dim_location.index + 1

# Merge keys into original DataFrame
df = df.merge(dim_institution, on=['Institution', 'Affiliation', 'AttendanceMode', 'Founded', 'Link'], how='left')
df = df.merge(dim_location, on=['City', 'Country', 'Continent'], how='left')

# Create fact_university_ranking
fact_university_ranking = df[['Rank', 'Enrollment', 'institution_id', 'location_id']].copy()
fact_university_ranking['id'] = fact_university_ranking.index + 1  # Optional primary key

# Reorder columns
fact_university_ranking = fact_university_ranking[['id', 'Rank', 'institution_id', 'location_id', 'Enrollment']]

dim_institution.to_csv("dim_institution.csv", index=False)
dim_location.to_csv("dim_location.csv", index=False)
fact_university_ranking.to_csv("fact_university_ranking.csv", index=False)

print("All data cleaned and transformed into fact and dimensions tables")