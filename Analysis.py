import pandas as pd
import glob
import os

def check_duplicates_in_csv(directory='.'):
    """Check CSV files in directory for duplicate rows and display results."""
    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    
    if not csv_files:
        print("No CSV files found in the directory.")
        return
    
    for csv_file in csv_files:
        print(f"\nChecking: {os.path.basename(csv_file)}")
        print("-" * 50)
        
        try:
            df = pd.read_csv(csv_file)
            total_rows = len(df)
            duplicate_count = df.duplicated().sum()
            
            if duplicate_count == 0:
                print(f"✓ No duplicates found ({total_rows} rows)")
            else:
                print(f"✗ Found {duplicate_count} duplicate row(s) out of {total_rows} rows")
                duplicates = df[df.duplicated(keep=False)].sort_values(by=list(df.columns))
                print("\nDuplicate rows:")
                print(duplicates)
        except Exception as e:
            print(f"Error reading file: {e}")

def check_blank_entries_in_csv(directory='.'):
    """Check CSV files for blank entries and show which columns are missing."""
    csv_files = glob.glob(os.path.join(directory, '*.csv'))

    if not csv_files:
        print("No CSV files found in the directory.")
        return

    for csv_file in csv_files:
        print(f"\nChecking: {os.path.basename(csv_file)}")
        print("-" * 50)

        try:
            df = pd.read_csv(csv_file)
            total_rows = len(df)

            # Treat both NaN and empty/whitespace strings as blank
            missing_mask = df.isnull() | df.astype(str).apply(lambda col: col.str.strip() == "")
            blank_entries_count = int(missing_mask.sum().sum())

            if blank_entries_count == 0:
                print(f"✓ No blank entries found ({total_rows} rows)")
            else:
                print(f"✗ Found {blank_entries_count} blank entry(ies) out of {total_rows} rows")

                rows_with_missing = missing_mask.any(axis=1)
                print("\nRows with blank entries and missing columns:")
                for row_idx in df.index[rows_with_missing]:
                    missing_columns = missing_mask.columns[missing_mask.loc[row_idx]].tolist()
                    print(f"Row {row_idx + 2}: missing -> {', '.join(missing_columns)}")

                print("\nAffected rows:")
                print(df.loc[rows_with_missing])

        except Exception as e:
            print(f"Error reading file: {e}")