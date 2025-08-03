"""
Indeed Job Scraper - Alternative Implementation
Scrapes job listings from Indeed and exports them to Indeed_Jobs.xlsx
This is a more reliable alternative as Indeed has better HTML structure for scraping
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin, quote_plus
import re

# Target Microsoft jobs on Indeed
COMPANY = "Microsoft"
LOCATION = "United States"
BASE_URL = "https://www.indeed.com/jobs"

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

def build_search_url(company, location, start=0):
    """Build Indeed search URL"""
    params = {
        "q": company,
        "l": location,
        "start": start
    }
    
    url = f"{BASE_URL}?q={quote_plus(company)}&l={quote_plus(location)}&start={start}"
    return url

def extract_job_data(job_card):
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
    
    try:
        # Extract job title
        title_elem = job_card.find("h2", class_="jobTitle")
        if title_elem:
            title_link = title_elem.find("a")
            if title_link:
                job_data["JobTitle"] = title_link.get("title", "").strip()
                # Extract job URL
                href = title_link.get("href", "")
                if href:
                    job_data["JobURL"] = urljoin("https://www.indeed.com", href)
        
        # Extract company (to verify it's Microsoft)
        company_elem = job_card.find("span", class_="companyName")
        company_name = ""
        if company_elem:
            company_link = company_elem.find("a")
            if company_link:
                company_name = company_link.get_text(strip=True)
            else:
                company_name = company_elem.get_text(strip=True)
        
        # Skip if not Microsoft job
        if "microsoft" not in company_name.lower():
            return None
        
        # Extract location
        location_elem = job_card.find("div", class_="companyLocation")
        if location_elem:
            job_data["Location"] = location_elem.get_text(strip=True)
        
        # Extract salary
        salary_elem = job_card.find("span", class_="salaryText")
        if salary_elem:
            job_data["Salary"] = salary_elem.get_text(strip=True)
        
        # Extract job summary/description
        summary_elem = job_card.find("div", class_="job-snippet")
        if summary_elem:
            summary_text = summary_elem.get_text(strip=True)
            job_data["JobDescriptionSummary"] = summary_text[:200] + "..." if len(summary_text) > 200 else summary_text
            
            # Try to extract experience from summary
            summary_lower = summary_text.lower()
            experience_patterns = [
                r'(\d+\+?\s*years?\s*(?:of\s*)?experience)',
                r'(entry\s*level)',
                r'(senior\s*level)',
                r'(junior\s*level)',
                r'(lead\s*position)',
                r'(principal\s*engineer)',
                r'(\d+\-\d+\s*years?)'
            ]
            
            for pattern in experience_patterns:
                match = re.search(pattern, summary_lower)
                if match:
                    job_data["ExperienceRequired"] = match.group(1).title()
                    break
            
            # Try to extract skills
            common_skills = [
                "python", "java", "javascript", "c++", "c#", "sql", "azure", "aws", 
                "react", "angular", "node.js", "docker", "kubernetes", "git",
                "machine learning", "ai", "data science", "cloud", "devops"
            ]
            
            found_skills = []
            for skill in common_skills:
                if skill in summary_lower:
                    found_skills.append(skill.title())
            
            if found_skills:
                job_data["SkillsRequired"] = ", ".join(found_skills[:5])  # Limit to 5 skills
        
        return job_data
        
    except Exception as e:
        print(f"Error extracting job data: {e}")
        return None

def get_job_listings(url):
    """Extract job listings from a page"""
    try:
        print(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="job_seen_beacon")
        
        jobs = []
        print(f"Found {len(job_cards)} job cards")
        
        for card in job_cards:
            job_data = extract_job_data(card)
            if job_data and job_data["JobTitle"]:  # Only add valid Microsoft jobs
                jobs.append(job_data)
        
        return jobs
        
    except Exception as e:
        print(f"Error getting job listings: {e}")
        return []

def main():
    all_jobs = []
    start = 0
    max_pages = 5
    page_count = 0
    
    print(f"🔍 Searching for {COMPANY} jobs on Indeed...")
    print(f"📍 Location: {LOCATION}")
    
    while page_count < max_pages:
        url = build_search_url(COMPANY, LOCATION, start)
        jobs = get_job_listings(url)
        
        if not jobs:
            print("No more jobs found or reached end of results")
            break
        
        all_jobs.extend(jobs)
        print(f"📄 Page {page_count + 1}: Found {len(jobs)} Microsoft jobs")
        
        page_count += 1
        start += 10  # Indeed shows 10 jobs per page
        
        # Be respectful to the server
        time.sleep(2)
    
    if all_jobs:
        # Create DataFrame and export to Excel
        df = pd.DataFrame(all_jobs, columns=COLUMNS)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['JobTitle', 'Location'])
        
        # Save to Excel
        output_file = f"{COMPANY}_Jobs.xlsx"
        df.to_excel(output_file, index=False, engine='openpyxl')
        
        print(f"\n✅ Successfully scraped {len(df)} unique {COMPANY} jobs!")
        print(f"📁 Data saved to: {output_file}")
        print(f"📊 Columns: {', '.join(COLUMNS)}")
        
        # Print statistics
        print(f"\n📈 Statistics:")
        print(f"  • Jobs with salary info: {len(df[df['Salary'] != ''])}")
        print(f"  • Jobs with experience requirements: {len(df[df['ExperienceRequired'] != ''])}")
        print(f"  • Jobs with skills listed: {len(df[df['SkillsRequired'] != ''])}")
        
        # Print sample
        if len(df) > 0:
            print(f"\n📋 Sample job listing:")
            sample = df.iloc[0]
            for col in COLUMNS:
                if sample[col]:
                    print(f"  • {col}: {sample[col]}")
                    
        return output_file
    else:
        print("❌ No jobs were found. Try adjusting the search parameters.")
        return None

if __name__ == "__main__":
    main()
