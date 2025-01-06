# import csv
# import re

# text = "Name of team members, problem statement, two potential ideas and completed Ideaspace worksheet due on Wednesday, November 6, 2024 11:59 PM EST."
# match = re.search(r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}(?: \d{1,2}:\d{2} (?:AM|PM) [A-Z]+)?', text)

# if match:
#     print("Matched date:", match.group())
# else:
#     print("No match found.")

# from datetime import datetime

# due_date_str = 'Friday, December 13, 2024 11:59 PM EST'
# # Remove the timezone part
# due_date_str_without_tz = ' '.join(due_date_str.split()[:-1])  # Removes 'EST'
# due_date_obj = datetime.strptime(due_date_str_without_tz, "%A, %B %d, %Y %I:%M %p")
# print("Parsed date:", due_date_obj)


from datetime import datetime
import pytz

due_date_str = 'Friday, December 13, 2024 11:59 PM EST'

# Define the date format without timezone for parsing
date_format_without_tz = "%A, %B %d, %Y %I:%M %p"

# Extract the datetime part and the timezone separately
date_part, tz_abbr = due_date_str.rsplit(' ', 1)

# Parse the datetime part
due_date_obj = datetime.strptime(date_part, date_format_without_tz)

# Map timezone abbreviation to a timezone object
timezone = pytz.timezone('US/Eastern')  # You can adjust this based on your location

# Localize the datetime object to the correct timezone
due_date_with_tz = timezone.localize(due_date_obj)
print("Parsed datetime with timezone:", due_date_with_tz)
