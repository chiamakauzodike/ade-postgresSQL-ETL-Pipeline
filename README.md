# ade-postgresSQL-ETL-Pipeline

University Data ETL Pipeline – Summary
This project automates the extraction, cleaning, and loading of university data from Wikipedia into a PostgreSQL database using Python.

🔄 Steps in the Pipeline:
Extract

Scrapes university ranking data from a Wikipedia page.

Transform (Clean)

Parses and formats Enrollment, Founded years, Location into City and Country.

Cleans missing or malformed fields.

Load

Uses a star schema:

dim_institution

dim_location

fact_university_ranking

Data is loaded into PostgreSQL using psycopg2 or SQLAlchemy.

🔧 Setup:
python3 -m venv venv
source venv/bin/activate

Python virtual environment with dependencies (requests, pandas, beautifulsoup4, psycopg2, dotenv).

.env file with PostgreSQL credentials.

PostgreSQL + pgAdmin for visualization and DB management.

🚀 How to Use:
Run the extract script to collect raw data.

Run the clean script to transform the data.

Run the load script to populate PostgreSQL tables.
