import pandas as pd
import sqlite3

def get_query_by_label(filename, label):
    """Extract a specific SQL query from a file using a label prefix."""
    with open(filename, "r") as f:
        content = f.read()

    queries = content.split("--")
    for q in queries:
        lines = q.strip().splitlines()
        if not lines:
            continue

        comment = lines[0].strip().lower()
        sql = "\n".join(lines[1:]).strip()

        if label.lower() in comment and sql:
            if sql.endswith(";"):
                sql = sql[:-1]
            return sql

    return None

def run_query(query, csv_file="urinalysis_tests.csv", table_name="urinalysis_tests"):
    """Execute a SQL query against CSV data loaded into in-memory SQLite."""
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_file}")
        return None
    except pd.errors.EmptyDataError:
        print(f"CSV file is empty: {csv_file}")
        return None
    except Exception as e:
        print(f"Failed to read CSV file: {e}")
        return None

    conn = sqlite3.connect(":memory:")
    try:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        result = pd.read_sql_query(query, conn)
        print(result)
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        conn.close()

def run_query_by_label(filename, label, csv_file="urinalysis_tests.csv"):
    """Find a SQL query by label in a file and execute it against the CSV data."""
    query = get_query_by_label(filename, label)
    if not query:
        print(f"No query found for label: {label}")
        return None

    return run_query(query, csv_file=csv_file)

def blank_entries(file):
    """Identify blank entries in the CSV file."""
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print(f"CSV file not found: {file}")
        return None
    except pd.errors.EmptyDataError:
        print(f"CSV file is empty: {file}")
        return None
    except Exception as e:
        print(f"Failed to read CSV file: {e}")
        return None

    blank_entries_df = df[df.isnull().any(axis=1)]
    print(blank_entries_df)
    return blank_entries_df

def duplicates(file):
    """Identify duplicate entries in the CSV file."""
    try:
        df = pd.read_csv(file)
    except FileNotFoundError:
        print(f"CSV file not found: {file}")
        return None
    except pd.errors.EmptyDataError:
        print(f"CSV file is empty: {file}")
        return None
    except Exception as e:
        print(f"Failed to read CSV file: {e}")
        return None
    
    duplicates_df = df[df.duplicated(keep=False)]
    if duplicates_df.empty:
        print("No duplicate entries found.")
    else:
        print(duplicates_df)
        
    return duplicates_df

