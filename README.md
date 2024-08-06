# Web-Scraper
This project is a Python-based web scraper designed to extract email addresses, names, and company names from specified websites. The primary purpose of this project is educational, allowing me to deepen my understanding of web scraping techniques and data extraction.


## Disclaimer
Important: I acknowledge that scraping websites to collect personal information such as emails, names, and company details can be unethical and potentially illegal, depending on jurisdiction and context. This project was developed purely for educational purposes and as an exercise in coding. I do not intend to use this tool for any malicious or unethical purposes.


## Features
* Extracts email addresses using regular expressions.
* Attempts to extract names and company names based on common HTML patterns.
* Ensures uniqueness of extracted emails to avoid duplicates in the output.
* Saves the collected data in a CSV file with columns for Name, Company, and Email.


## How It Works
1. Email Extraction: Uses a regular expression to find email patterns within the text of a webpage.
2. Name and Company Extraction: Attempts to extract names and company names using meta tags, title tags, and common heading tags. This part of the extraction is heuristic and may not always be accurate.


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/web-scraper.git
   cd web-scraper

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt


## Usage
1. Add the URLs of the websites you want to scrape in the urls list in the main function.
2. Run the script.
3. The results will be saved in emails.csv (Please use or export the data from the emails.csv file before rerunning the code, as the file's contents will be overwritten each time the script is executed)



> **Note**:  
> This script was created with the assistance of GPT-4, an advanced language model developed by OpenAI. GPT-4 was used to ensure best practices in web scraping, error handling, correct library utilization, and data extraction.
