import csv
import re

text = "Name of team members, problem statement, two potential ideas and completed Ideaspace worksheet due on Wednesday, November 6, 2024 11:59 PM EST."
match = re.search(r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday),\s(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}(?: \d{1,2}:\d{2} (?:AM|PM) [A-Z]+)?', text)

if match:
    print("Matched date:", match.group())
else:
    print("No match found.")
