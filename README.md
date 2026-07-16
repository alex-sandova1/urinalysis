# Clinical Laboratory Data Analysis & Urinalysis Quality Analytics

## Project Motivation

Laboratory environments rely on accurate data collection, quality control processes, and consistent interpretation of test results. This project explores how data analytics can support laboratory workflows by organizing clinical measurements, identifying abnormal patterns, and improving visibility into sample-level trends.

The project reflects the intersection of laboratory quality practices and data science methodologies.

This project analyzes a dataset containing 1000+ urinalysis records and applies data analytics and quality analysis techniques to identify trends, detect abnormal results, and visualize laboratory findings.

## Overview

This project applies data analytics and quality analysis techniques to clinical urinalysis data to identify trends, detect abnormal results, and visualize laboratory findings.

The project was designed to simulate a laboratory data review workflow by combining:
- Data cleaning and validation
- SQL-based analysis
- Clinical parameter evaluation
- Interactive dashboard visualization

The goal is to demonstrate how data science techniques can support quality-focused decision making in laboratory and healthcare environments.

## Project Structure

- `Main.py`: Launches the dashboard UI
- `Analysis.py`: Query runner and data quality helpers (`blank_entries`, `duplicates`)
- `Test.py`: Example analysis script that executes all labeled queries
- `Queries.sql`: Named SQL query blocks
- `DATA_QUALITY_NOTES.md`: Reference rules used to classify abnormal samples
- `urinalysis_tests.csv`: Dataset

## Quality Analytics Workflow

1. Data Validation
   - Identifies blank records and duplicate samples
   - Reviews data consistency before analysis

2. Laboratory Data Processing
   - Converts raw urinalysis results into structured analytical data
   - Applies documented laboratory reference thresholds to classify samples based on abnormal findings.

3. Exploratory Analysis
   - Examines relationships between laboratory parameters and diagnoses
   - Identifies trends across chemistry and microscopy results

4. Reporting Dashboard
   - Provides interactive summaries for reviewing sample results
   - Allows filtering and exporting of analyzed data


## Laboratory Parameters

The dataset includes chemistry and microscopy measurements including:

### Chemistry
- Glucose
- Protein
- pH
- Specific Gravity

### Microscopy
- WBC
- RBC
- Epithelial Cells
- Mucus Threads
- Amorphous Urates
- Bacteria

### Classification
- Reported diagnosis category
- Laboratory result classification (Normal/Abnormal)

## Technologies

### Programming & Data Analysis
- Python
- Pandas
- SQL
- SQLite

### Visualization & Interface
- Matplotlib
- Tkinter

### Data Analytics Methods
- Data Cleaning
- Exploratory Data Analysis (EDA)
- Data Quality Validation
- Laboratory Parameter Analysis
- Rule-Based Classification

## Features

### Dashboard (`Main.py`)

- Computes `Overall Status` (Normal/Abnormal) from urinalysis thresholds and categorical rules
- Filter by diagnosis (`All results`, `NEGATIVE`, `POSITIVE`)
- Search by generated sample ID (`SMP-00001`, etc.)
- KPI cards for totals, normal/abnormal counts, and positive results
- Charts for:
	- Abnormal samples by parameter
	- Samples by lab result
	- Parameter distribution (normal vs abnormal)
- Key averages (pH, specific gravity, WBC, RBC, protein/glucose positive rate)
- Recent samples table
- Full filtered dataset window via:
	- `View all samples`
	- Sidebar `Patient Samples`
- Export filtered data to CSV

### Script Analysis (`Test.py` + `Analysis.py`)

- Loads CSV into in-memory SQLite
- Runs predefined labeled SQL queries from `Queries.sql`
- Prints grouped summaries (gender, age group, diagnosis, chemistry and microscopy fields)
- Detects blank rows and duplicate rows

## Requirements

- Python 3.10+
- `pandas`

Install dependencies:

```bash
pip install pandas
```

## Run

Run the dashboard:

```bash
python Main.py
```

Run the script-based analysis:

```bash
python Test.py
```

If you use the project virtual environment, use the interpreter from `.venv`.

## Key Insights

The analysis identifies relationships between laboratory parameters and abnormal sample classifications, including trends in:
- Elevated WBC and bacterial indicators
- Protein and glucose abnormalities
- RBC distributions
- Chemistry and microscopy result patterns

## Data Notes

- The abnormal status logic in the dashboard follows thresholds documented in `DATA_QUALITY_NOTES.md`.
- Sample IDs displayed in the UI are derived from `ID` as `SMP-` plus zero-padded numeric value.

## Future Improvements

- Develop classification models to predict abnormal laboratory patterns
- Evaluate feature importance of urinalysis parameters
- Perform statistical analysis between patient groups
- Add interactive filtering with additional visualization libraries
- Generate automated laboratory quality reports