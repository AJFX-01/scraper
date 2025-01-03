import csv

# Input and output file paths
file_path = "output4.csv"  # Use the file where rows have already been removed

# Read the file and update the "No" column
with open(file_path, mode="r") as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)  # Load all rows into memory
    fieldnames = reader.fieldnames  # Get column headers

# Update the "No" column sequentially
for i, row in enumerate(rows, start=1):
    row['No'] = i

# Write the updated rows back to the same file
with open(file_path, mode="w", newline="") as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()  # Write the header
    writer.writerows(rows)  # Write the updated rows

print(f"'No' column updated sequentially in '{file_path}'.")
