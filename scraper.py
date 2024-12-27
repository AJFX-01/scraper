import subprocess

def send_to_group(data):
  message = f"Hi, Group! Here's the lastest update from the dashboard\n\n{data}"
  subprocess.run(["node", "send-group-message.js", message])

def main():
  scraped_data = scraped_data
  formatted_data = "\n".join(scraped_data[:5])
  send_to_group(formatted_data)



if __name__ == "__main__":
  main()