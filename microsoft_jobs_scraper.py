"""
Microsoft Careers Page Scraper
Scrapes job listings and exports them to Microsoft_Jobs.xlsx
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from urllib.parse import urljoin

# We'll use Microsoft's API endpoint for more reliable data
BASE_URL = "https://careers.microsoft.com/professionals/us/en/search-results"
API_URL = "https://careers.microsoft.com/professionals/us/en/search-results"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# Data columns
COLUMNS = [
    "JobTitle",
    "Location",
    "ExperienceRequired",
    "SkillsRequired",
    "Salary",
    "JobURL",
    "JobDescriptionSummary"
]

def get_job_listings(page_url):
    """Extract job listings from a page"""
    try:
        response = requests.get(page_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = []
        
        # Try multiple possible selectors for job cards
        job_cards = (soup.find_all("div", class_="job-tile") or 
                    soup.find_all("div", class_="job-card") or
                    soup.find_all("article", class_="job") or
                    soup.find_all("div", attrs={"data-ph-at-id": "job-item"}))
        
        print(f"Found {len(job_cards)} job cards on this page")
        
        for card in job_cards:
            job_data = extract_job_data(card)
            if job_data["JobTitle"]:  # Only add if we have at least a title
                jobs.append(job_data)
        
        return jobs
    except Exception as e:
        print(f"Error getting job listings: {e}")
        return []

def extract_job_data(card):
    """Extract data from a single job card"""
    job_data = {
        "JobTitle": "",
        "Location": "",
        "ExperienceRequired": "",
        "SkillsRequired": "",
        "Salary": "",
        "JobURL": "",
        "JobDescriptionSummary": ""
    }
    
    # Extract title
    title_selectors = ["h2", "h3", ".job-title", "[data-ph-at-id='job-title']", "a[href*='job']"]
    for selector in title_selectors:
        title_elem = card.select_one(selector)
        if title_elem:
            job_data["JobTitle"] = title_elem.get_text(strip=True)
            break
    
    # Extract location
    location_selectors = [".job-location", ".location", "[data-ph-at-id='job-location']", 
                         "*[class*='location']", "*[class*='city']"]
    for selector in location_selectors:
        location_elem = card.select_one(selector)
        if location_elem:
            job_data["Location"] = location_elem.get_text(strip=True)
            break
    
    # Extract job URL
    link_elem = card.find("a", href=True)
    if link_elem:
        href = link_elem["href"]
        if href.startswith("http"):
            job_data["JobURL"] = href
        else:
            job_data["JobURL"] = urljoin("https://careers.microsoft.com", href)
    
    # Extract description/summary
    desc_selectors = [".job-description", ".job-excerpt", ".job-summary", "p"]
    for selector in desc_selectors:
        desc_elem = card.select_one(selector)
        if desc_elem:
            desc_text = desc_elem.get_text(strip=True)
            if len(desc_text) > 20:  # Only take meaningful descriptions
                job_data["JobDescriptionSummary"] = desc_text[:200] + "..." if len(desc_text) > 200 else desc_text
                break
    
    # Look for experience/skills in text content
    card_text = card.get_text().lower()
    
    # Extract experience requirements
    experience_keywords = ["years", "experience", "senior", "junior", "entry", "lead", "principal"]
    for keyword in experience_keywords:
        if keyword in card_text:
            # Try to extract the experience requirement
            sentences = card.get_text().split(".")
            for sentence in sentences:
                if keyword in sentence.lower() and len(sentence) < 100:
                    job_data["ExperienceRequired"] = sentence.strip()
                    break
            if job_data["ExperienceRequired"]:
                break
    
    return job_data

def get_next_page(soup, current_url):
    """Find the next page URL"""
    try:
        # Look for pagination elements
        next_selectors = [
            "a[aria-label*='next']",
            "a[title*='next']", 
            ".pagination a:contains('Next')",
            ".pagination a:contains('>')",
            "a[href*='page']"
        ]
        
        for selector in next_selectors:
            next_elem = soup.select_one(selector)
            if next_elem and next_elem.get("href"):
                next_url = next_elem["href"]
                if not next_url.startswith("http"):
                    next_url = urljoin(current_url, next_url)
                return next_url
        
        return None
    except Exception as e:
        print(f"Error finding next page: {e}")
        return None

def main():
    all_jobs = []
    page_url = BASE_URL
    page_count = 0
    max_pages = 5  # Limit to prevent infinite loops
    
    print("Starting Microsoft careers page scraping...")
    
    while page_url and page_count < max_pages:
        page_count += 1
        print(f"Scraping page {page_count}: {page_url}")
        
        try:
            response = requests.get(page_url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            jobs = get_job_listings(page_url)
            all_jobs.extend(jobs)
            
            print(f"Found {len(jobs)} jobs on page {page_count}")
            
            # Check for next page
            next_page = get_next_page(soup, page_url)
            if next_page and next_page != page_url:  # Avoid infinite loops
                page_url = next_page
                time.sleep(2)  # Be respectful to the server
            else:
                print("No more pages found")
                break
                
        except Exception as e:
            print(f"Error on page {page_count}: {e}")
            break
    
    if all_jobs:
        # Create DataFrame and export to Excel
        df = pd.DataFrame(all_jobs, columns=COLUMNS)
        
        # Clean up the data
        df = df.drop_duplicates(subset=['JobTitle', 'Location'])  # Remove duplicates
        df = df[df['JobTitle'].str.len() > 0]  # Remove entries without titles
        
        # Save to Excel
        output_file = "Microsoft_Jobs.xlsx"
        df.to_excel(output_file, index=False, engine='openpyxl')
        
        print(f"\n✅ Successfully scraped {len(df)} unique jobs!")
        print(f"📁 Data saved to: {output_file}")
        print(f"📊 Columns: {', '.join(COLUMNS)}")
        
        # Print sample data
        if len(df) > 0:
            print(f"\n📋 Sample job listing:")
            for col in COLUMNS:
                if df.iloc[0][col]:
                    print(f"  {col}: {df.iloc[0][col]}")
    else:
        print("❌ No jobs were scraped. The website structure may have changed.")
        print("💡 Try checking the website manually or updating the selectors.")

if __name__ == "__main__":
    main()
