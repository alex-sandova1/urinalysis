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

if __name__ == "__main__":
	main()