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
    # Load the exisiting data to vaiod duplicates
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
            title = row.get('title', '').lower()
            if 'due' in title.lower():
                # Extract the date from the file using regex pattern
                date_match = re.search(
                    r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}',
                    title)
                if date_match:
                    due_date_str = date_match.group(0)
                    try:
                        # Parse the date
                        due_date_obj = datetime.strptime(due_date_str, "%B %d, %Y")
                        if due_date_obj >= datetime.now():
                            row_tuple = (row["No"], title, due_date_str)
                            if row_tuple not in existing_rows:
                                filtered_rows.append({"No": row["No"], "title" : title,
                                                      "duedate":due_date_str})
                                existing_rows.add(row_tuple)
                    except ValueError:
                        print(f"Skipping row with invalid date: {title}")

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
    scraper()
    # scraped_data = scraper()
    # formatted_data = "\n".join(scraped_data)
    # send_to_group(formatted_data)




if __name__ == "__main__":
    main()


