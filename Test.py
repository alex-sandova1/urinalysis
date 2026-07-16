from Analysis import *

def main():
	# Define the path to the CSV file containing urinalysis test data
	csv_file = "urinalysis_tests.csv"

	run_query_by_label("Queries.sql", "Number of urinalysis tests by gender")
	print("\n")
	blank_entries(csv_file)
	print("\n")
	duplicates(csv_file)
	print("\n")
	run_query_by_label("Queries.sql", "Number of urinalysis tests by age group")
	print("\n")
	run_query_by_label("Queries.sql", "Number of urinalysis tests by diagnosis")
	print("\n")
	run_query_by_label("Queries.sql", "Group by urine color")
	print("\n")
	run_query_by_label("Queries.sql", "Group by urine clarity")
	print("\n")
	run_query_by_label("Queries.sql", "Group by Glucose")
	print("\n")
	run_query_by_label("Queries.sql", "Group by Protein")
	print("\n")
	run_query_by_label("Queries.sql", "Group by pH")
	print("\n")
	run_query_by_label("Queries.sql", "Group by Specific Gravity")
	print("\n")
	run_query_by_label("Queries.sql", "Group by WBC")
	print("\n")
	run_query_by_label("Queries.sql", "Group by RBC")
	print("\n")
	run_query_by_label("Queries.sql", "Group by Epithelial Cells")
	print("\n")
	run_query_by_label("Queries.sql", "Group by Bacteria")
	print("\n")
	run_query_by_label("Queries.sql", "Group by Mucous Threads")
	print("\n")
	run_query_by_label("Queries.sql", "Group by Amorphous Urates")
	print("\n")

if __name__ == "__main__":
	main()