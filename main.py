import requests
from bs4 import BeautifulSoup
import csv
import re

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    print(f"Extracted emails: {emails}")
    return emails

def extract_phone_numbers(text):
    phone_pattern = r'\(?\b\d{3}[-.)\s]?\d{3}[-.\s]?\d{4}\b'
    phone_numbers = re.findall(phone_pattern, text)
    print(f"Extracted phone numbers: {phone_numbers}")
    return phone_numbers

def extract_name(soup):
    name_tag = soup.find('meta', attrs={'name': 'author'})
    if name_tag:
        return name_tag.get('content', None)
    
    h1_tag = soup.find('h1')
    if h1_tag:
        return h1_tag.text.strip()
    
    return 'Name Not Found'

def extract_company(soup):
    title_tag = soup.find('title')
    if title_tag:
        return title_tag.text.strip()
    
    company_meta = soup.find('meta', attrs={'property': 'og:site_name'})
    if company_meta:
        return company_meta.get('content', None)
    
    return 'Company Not Found'

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        print(f"Fetched content from {url}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None, None, [], []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    
    emails = extract_emails(text)
    phone_numbers = extract_phone_numbers(text)
    
    name = extract_name(soup)
    company = extract_company(soup)
    
    return name, company, emails, phone_numbers

def save_to_csv(data, filename='contacts.csv'):
    # Specify the full path where you want to save the CSV file
    full_path = f'd:/Ontario Tech University/GitHub Assignments/Web-Scraper/{filename}'
    
    if not data:
        print("No data to save.")
    else:
        with open(full_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Company', 'Email', 'Phone Number'])
            for row in data:
                writer.writerow(row)
        print(f"Data saved to {full_path}")



def main(urls):
    data = []
    seen_emails = set()
    seen_phone_numbers = set()
    
    for url in urls:
        url = url.strip()  
        print(f"Processing {url}")
        
        name, company, emails, phone_numbers = scrape_website(url)
        
        if not emails and not phone_numbers:
            print(f"No data found for {url}")
            continue
        
        for email in emails:
            if email not in seen_emails:
                seen_emails.add(email)
                data.append([name, company, email, ''])
        
        for phone_number in phone_numbers:
            if phone_number not in seen_phone_numbers:
                seen_phone_numbers.add(phone_number)
                data.append([name, company, '', phone_number])
    
    if data:
        save_to_csv(data)
    else:
        print("No data to save.")

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
