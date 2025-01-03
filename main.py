import subprocess
# from .scraper import scraper
from scrpt import scraper

# def send_to_group(data):
#   message = f"Hi, Guys!\n{data}"
#   subprocess.run(["node", "sendmessage.js", message])

def main():
  scraper()
  # scraped_data = scraper()
  # formatted_data = "\n".join(scraped_data)
  # send_to_group(formatted_data)




if __name__ == "__main__":
  main()


