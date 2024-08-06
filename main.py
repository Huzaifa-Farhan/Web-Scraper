import requests
from bs4 import BeautifulSoup
import csv
import re

def extract_emails(text):
    # Define a regular expression pattern for extracting emails
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    # Use re.findall to find all occurrences of the pattern in the text
    return re.findall(email_pattern, text)

def extract_name(soup):
    # Example logic to extract a name (this can vary widely depending on the site)
    name = None
    # Try to extract name from meta tags or specific headings
    name_tag = soup.find('meta', attrs={'name': 'author'})
    if name_tag:
        name = name_tag.get('content', None)
    if not name:
        h1_tag = soup.find('h1')
        if h1_tag:
            name = h1_tag.text.strip()
    return name or 'Name Not Found'

def extract_company(soup):
    # Example logic to extract a company name (again, this can vary)
    company = None
    title_tag = soup.find('title')
    if title_tag:
        company = title_tag.text.strip()
    # Additional checks for known sections or tags
    if not company:
        company_meta = soup.find('meta', attrs={'property': 'og:site_name'})
        if company_meta:
            company = company_meta.get('content', None)
    return company or 'Company Not Found'

def scrape_website(url):
    try:
        # Send a GET request to the specified URL
        response = requests.get(url)
        # Raise an HTTPError for bad responses (4xx and 5xx)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # Print an error message if the request fails
        print(f"Error fetching {url}: {e}")
        return None, None, []  # Return None for name/company and empty list for emails
    
    # Parse the website's HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract all the text from the parsed HTML
    text = soup.get_text()
    # Extract emails from the text using the extract_emails function
    emails = extract_emails(text)
    # Extract name and company using their respective functions
    name = extract_name(soup)
    company = extract_company(soup)
    return name, company, emails

def save_to_csv(data, filename='emails.csv'):
    # Open a new CSV file for writing
    with open(filename, mode='w', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file)
        # Write the header row to the CSV file
        writer.writerow(['Name', 'Company', 'Email'])
        # Write each row of data to the CSV file
        for row in data:
            writer.writerow(row)

def main(urls):
    data = []  # Initialize a list to store the collected data
    seen_emails = set()  # Initialize a set to store unique emails
    
    # Loop through each URL in the list of URLs
    for url in urls:
        # Scrape the website and extract name, company, and emails
        name, company, emails = scrape_website(url)
        # Loop through each extracted email
        for email in emails:
            # Check if the email is not already in the seen_emails set
            if email not in seen_emails:
                # Add the email to the set to ensure uniqueness
                seen_emails.add(email)
                # Add a new row to the data list with extracted Name, Company, and Email
                data.append([name, company, email])
    
    # Save the collected data to a CSV file
    save_to_csv(data)

if __name__ == '__main__':
    # List of websites to scrape; replace with your target URLs
    urls = [
        'example url #1'
        'example url #2'
        'example url #3'
        # Add more URLs as needed
    ]
    # Call the main function with the list of URLs
    main(urls)
