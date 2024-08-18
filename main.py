import requests
from bs4 import BeautifulSoup
import csv
import re

# Function to extract emails from a given text
def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    print(f"Extracted emails: {emails}")
    return emails

# Function to extract phone numbers from a given text
def extract_phone_numbers(text):
    phone_pattern = r'\(?\b\d{3}[-.)\s]?\d{3}[-.\s]?\d{4}\b'
    phone_numbers = re.findall(phone_pattern, text)
    print(f"Extracted phone numbers: {phone_numbers}")
    return phone_numbers

# Function to extract the name of the person or entity from the HTML
def extract_name(soup):
    # Try to find the name in the meta tag with name 'author'
    name_tag = soup.find('meta', attrs={'name': 'author'})
    if name_tag:
        return name_tag.get('content', None)
    
    # Try to find the name in the first <h1> tag
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.text.strip()
    
    return 'Name Not Found'

# Function to extract the company name from the HTML
def extract_company(soup):
    # Try to find the company name in the <title> tag
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.text.strip()
    
    # Try to find the company name in the meta tag with property 'og:site_name'
    company_meta = soup.find('meta', attrs={'property': 'og:site_name'})
    if company_meta:
        return company_meta.get('content', None)
    
    return 'Company Not Found'

# Function to scrape data from a given website URL
def scrape_website(url):
    try:
        # Fetch the content of the URL
        response = requests.get(url)
        response.raise_for_status()
        print(f"Fetched content from {url}")
    except requests.exceptions.RequestException as e:
        # Handle errors if any occur during the request
        print(f"Error fetching {url}: {e}")
        return None, None, [], []
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    
    # Extract emails and phone numbers from the text
    emails = extract_emails(text)
    phone_numbers = extract_phone_numbers(text)
    
    # Extract the name and company from the HTML
    name = extract_name(soup)
    company = extract_company(soup)
    
    return name, company, emails, phone_numbers

# Function to save the extracted data to a CSV file
def save_to_csv(data, filename='contacts.csv'):
    # Specify the full path where you want to save the CSV file
    full_path = f'd:/Ontario Tech University/GitHub Assignments/Web-Scraper/{filename}'
    
    if not data:
        print("No data to save.")
    else:
        # Open the file in write mode and create a CSV writer object
        with open(full_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Company', 'Email', 'Phone Number'])
            for row in data:
                writer.writerow(row)
        print(f"Data saved to {full_path}")

# Main function to process a list of URLs
def main(urls):
    data = []
    seen_emails = set()
    seen_phone_numbers = set()
    
    for url in urls:
        url = url.strip()  # Remove any leading or trailing whitespace
        print(f"Processing {url}")
        
        # Scrape the website for data
        name, company, emails, phone_numbers = scrape_website(url)
        
        if not emails and not phone_numbers:
            print(f"No data found for {url}")
            continue
        
        # Add unique emails to the data list
        for email in emails:
            if email not in seen_emails:
                seen_emails.add(email)
                data.append([name, company, email, ''])
        
        # Add unique phone numbers to the data list
        for phone_number in phone_numbers:
            if phone_number not in seen_phone_numbers:
                seen_phone_numbers.add(phone_number)
                data.append([name, company, '', phone_number])
    
    # Save the collected data to a CSV file
    if data:
        save_to_csv(data)
    else:
        print("No data to save.")

# Entry point of the script
if __name__ == '__main__':
    urls = [
        'https://www.boardwalkburgers.ca/',
        'https://indraprasthaindiancuisinewhitby.com/',
        'https://www.thevaultwhitby.com/',
        'https://www.bollockspub.com/',
        'https://www.billiejax.com/',
        'https://www.instagram.com/blackjackbarandgrill/?igshid=MzRlODBiNWFlZA%3D%3D',
        'https://www.charleyronicks.ca/',
        'http://www.atavolabistro.com/',
        'https://theoakandale.com/',
        'https://www.12welvebistro.ca/',
        'https://chucksroadhouse.com/',
        'https://www.smashkitchen.com/',
        'https://bigbonebbq.ca/big-bone-bbq-whitby/',
        'https://www.thespringwoodwhitby.com/',
        'https://www.thebrockhouse.ca/',
        'https://www.butchies.ca/',
        'https://www.mehfill.ca/'
    ]
    main(urls)
