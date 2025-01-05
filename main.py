import subprocess
import csv
# from .scraper import scraper
from scrpt import scraper

# def send_to_group(data):
#   message = f"Hi, Guys!\n{data}"
#   subprocess.run(["node", "sendmessage.js", message])

def save_duedate() ->  str:
    """ Store Upcoming Due Dates in a new csv"""
    # iterated over the csv files and check for due dates
    # if the due date is less is before current date we ignore
    # else if the due date is after the current date,
    # we save update the current csv called upcoming duedate.csv
    return "csv"

def filter_csv() -> str:
    """ filter csv """
    # transverse the csv and check for things like "Quiz "" updated. Your grade is"
    # if the dcsv contaians it we ignore and remove it from the messages to be sent to the group
    return "updated"

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


