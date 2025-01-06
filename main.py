""" Main.py """

import os
import re
from datetime import datetime
import subprocess
import csv
# from .scraper import scraper
from scrpt import scraper

# def send_to_group(data):
#   message = f"Hi, Guys!\n{data}"
#   subprocess.run(["node", "sendmessage.js", message])

def save_duedate(input_csv: str, output_csv: str):
    """ Store Upcoming Due Dates 
        Into the upcoming.csv
        appending to an existing file.
        iterated over the csv files and check for due dates
        if the due date is less is before current date we ignore
        else if the due date is after the current date,
        we save update the current csv called upcoming duedate.csv
    """
    existing_rows = set()
    # Load the exisiting data to avoid duplicates
    if os.path.exists(output_csv):
        with open(output_csv, mode="r", encoding="utf-8") as exisiting_file:
            exisiting_reader = csv.DictReader(exisiting_file)
            existing_rows = {tuple(row.values()) for row in exisiting_reader}

    # Open the input data to read rows
    with open(input_csv, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = ["No", "title", "duedate"] # Geat columns headers

        filtered_rows = []
        for row in reader:
            title = row.get('title', '').strip()
            if 'due' in title.lower():
                # Extract the date from the file using regex pattern
                date_match = re.search(
                    r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}(?: \d{1,2}:\d{2} (?:AM|PM) [A-Z]+)?',
                    title)
                if date_match:
                    due_date_str = date_match.group(0)
                    try:
                        # Parse the data
                        print(due_date_str)
                        due_date_obj = datetime.strptime(due_date_str, "%B %d, %Y")
                        if due_date_obj >= datetime.now():
                            row_tuple = (row["No"], title, due_date_str)
                            if row_tuple not in existing_rows:
                                filtered_rows.append({"No": row["No"], "title" : title,
                                                      "duedate":due_date_str})
                                existing_rows.add(row_tuple)
                    except ValueError:
                        print(f"Skipping row with invalid date: {title}")
                else:
                    print("No date matches found")

    # Append new Data to output CSV
    with open(output_csv, mode="a", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        if os.stat(output_csv).st_size == 0:
            writer.writeheader()
        writer.writerows(filtered_rows)
    print(f"upcoming due dates added to : {output_csv}")


def filter_csv(data_file : str) -> str:
    # transverse the csv and check for things like "Quiz "" updated. Your grade is"
    # if the dcsv contaians it we ignore and remove it from the messages to be sent to the group
    """Remove rows containing 'Your grade is' in the title column."""
    temp_file = "temp_cleaned.csv"
    with open(data_file, mode="r", encoding="utf-8") as infile, \
      open(temp_file, mode="w", encoding="utf-8", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError(f"Invalid CSV format in {data_file}")
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if "your grade is:" not in row.get("title", "").lower():
                writer.writerow(row)
    os.replace(temp_file, data_file)

def remove_duplicates(base_file: str, new_file: str) -> str:
    """Merge base_file and new_file without duplicates, updating base_file only with unique rows.
    Return new rows found as a string without the 'No' column."""
    temp_output_file = "merged_output.csv"
    base_data = set()
    new_data = set()
    fieldnames = []

    # Load data from base_file
    if os.path.exists(base_file):
        with open(base_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            if not fieldnames or "No" not in fieldnames:
                return "Invalid CSV format in base file."
            for row in reader:
                # Exclude "No" column when storing data
                base_data.add(tuple(row[col] for col in fieldnames if col != "No"))

    # Load data from new_file
    if os.path.exists(new_file):
        with open(new_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames or reader.fieldnames != fieldnames:
                return "CSV headers do not match between files."
            for row in reader:
                # Exclude "No" column when storing data
                new_data.add(tuple(row[col] for col in fieldnames if col != "No"))

    # Find unique rows in new_file that are not in base_file
    unique_new_data = new_data - base_data
    if not unique_new_data:
        return "No new message"

    # Merge base data and unique new data
    all_data = base_data | unique_new_data

    # Write merged data back to base_file
    with open(temp_output_file, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for index, row in enumerate(all_data, start=1):
            writer.writerow(dict(zip(fieldnames, [str(index)] + list(row))))

    os.replace(temp_output_file, base_file)

    # Prepare output string of new rows without 'No' column
    result_lines = ["\n".join(", ".join(row) for row in unique_new_data)]
    return "\n".join(result_lines)

def send_upcoming_duedate() -> str:
    """ send upcoming due dates """
    # we have a background task runing every morning to chek the upcoming
    # due dates we have in a csv
    # if it upcoming in 3 days times we send it
    # also we do the same for 2 says times
    # also we do the same for 1 days times
    # and finally on the D-day
    return "due "

def main():
    """ where the function runs """
    save_duedate("due.csv", "upcoming.csv")
    # scraped_data = scraper()
    # formatted_data = "\n".join(scraped_data)
    # send_to_group(formatted_data)




if __name__ == "__main__":
    main()
