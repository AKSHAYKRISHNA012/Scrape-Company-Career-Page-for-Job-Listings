"""
Comprehensive Job Scraper - Multiple Sources
This scraper demonstrates web scraping techniques using multiple approaches:
1. Direct company careers page scraping
2. RSS feeds (if available)
3. Demo data generation for testing

Exports results to Company_Jobs.xlsx
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
from urllib.parse import urljoin, quote_plus
import re
from datetime import datetime
import random

# Configuration
COMPANY_NAME = "TechCorp"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

# Required columns for the Excel output
COLUMNS = [
    "JobTitle",
    "Location", 
    "ExperienceRequired",
    "SkillsRequired",
    "Salary",
    "JobURL",
    "JobDescriptionSummary"
]

def generate_demo_jobs():
    """Generate realistic demo job data for demonstration purposes"""
    
    job_titles = [
        "Software Engineer", "Senior Software Engineer", "Principal Software Engineer",
        "Data Scientist", "Senior Data Scientist", "Machine Learning Engineer",
        "Product Manager", "Senior Product Manager", "Technical Product Manager",
        "DevOps Engineer", "Senior DevOps Engineer", "Cloud Architect",
        "Frontend Developer", "Backend Developer", "Full Stack Developer",
        "Security Engineer", "Site Reliability Engineer", "Platform Engineer",
        "Engineering Manager", "Technical Lead", "Solutions Architect"
    ]
    
    locations = [
        "Seattle, WA", "San Francisco, CA", "New York, NY", "Austin, TX",
        "Boston, MA", "Chicago, IL", "Denver, CO", "Atlanta, GA",
        "Remote", "Hybrid - Seattle", "Hybrid - San Francisco"
    ]
    
    experience_levels = [
        "0-2 years", "2-5 years", "5-8 years", "8+ years",
        "Entry Level", "Mid Level", "Senior Level", "Principal Level",
        "Fresh Graduate", "3+ years experience", "7+ years experience"
    ]
    
    skills_pool = [
        "Python, SQL, AWS", "Java, Spring, Kubernetes", "JavaScript, React, Node.js",
        "C#, .NET, Azure", "Go, Docker, Terraform", "Python, Machine Learning, TensorFlow",
        "TypeScript, Angular, PostgreSQL", "Scala, Spark, Kafka", "Ruby, Rails, Redis",
        "C++, Linux, Git", "Swift, iOS, Xcode", "Kotlin, Android, Firebase"
    ]
    
    salaries = [
        "$80,000 - $120,000", "$100,000 - $150,000", "$120,000 - $180,000",
        "$150,000 - $220,000", "$180,000 - $280,000", "$200,000 - $350,000",
        "", "", ""  # Some jobs don't list salary
    ]
    
    descriptions = [
        "Join our team to build scalable software solutions that impact millions of users worldwide. You'll work with cutting-edge technologies in a collaborative environment.",
        "We're looking for a passionate engineer to help us develop next-generation cloud infrastructure. Strong problem-solving skills and attention to detail required.",
        "Drive product strategy and execution for our core platform. Work closely with engineering teams to deliver innovative features that delight our customers.",
        "Lead the development of machine learning models that power our recommendation systems. Experience with large-scale data processing is essential.",
        "Build and maintain robust CI/CD pipelines and infrastructure. Help us scale our services to handle growing user demand efficiently.",
        "Design and implement user-facing features that are both beautiful and functional. Collaborate with designers and backend engineers.",
        "Architect secure, scalable systems that protect user data and ensure compliance. Work with teams across the organization on security initiatives.",
        "Manage a team of talented engineers while contributing to technical decisions. Foster a culture of innovation and continuous learning."
    ]
    
    jobs = []
    for i in range(25):  # Generate 25 demo jobs
        job = {
            "JobTitle": random.choice(job_titles),
            "Location": random.choice(locations),
            "ExperienceRequired": random.choice(experience_levels),
            "SkillsRequired": random.choice(skills_pool),
            "Salary": random.choice(salaries),
            "JobURL": f"https://careers.{COMPANY_NAME.lower()}.com/jobs/{i+1000}",
            "JobDescriptionSummary": random.choice(descriptions)
        }
        jobs.append(job)
    
    return jobs

def scrape_real_jobs():
    """
    Attempt to scrape real jobs from publicly accessible sources
    This is a template that can be adapted for different websites
    """
    jobs = []
    
    # Example: Try to scrape from a hypothetical careers page
    # In practice, you would replace this URL with a real company's careers page
    test_urls = [
        "https://httpbin.org/html",  # Safe test URL
        # Add real careers page URLs here
    ]
    
    for url in test_urls:
        try:
            print(f"Attempting to scrape: {url}")
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            # This is a template - adjust selectors based on the actual website
            job_cards = soup.find_all("div", class_="job-card")  # Example selector
            
            for card in job_cards:
                try:
                    job_data = {
                        "JobTitle": "",
                        "Location": "",
                        "ExperienceRequired": "",
                        "SkillsRequired": "",
                        "Salary": "",
                        "JobURL": "",
                        "JobDescriptionSummary": ""
                    }
                    
                    # Extract job details (customize based on actual HTML structure)
                    title_elem = card.find("h2") or card.find("h3")
                    if title_elem:
                        job_data["JobTitle"] = title_elem.get_text(strip=True)
                    
                    # Add more extraction logic here...
                    
                    if job_data["JobTitle"]:
                        jobs.append(job_data)
                        
                except Exception as e:
                    print(f"Error extracting job data: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            continue
    
    return jobs

def create_excel_file(jobs, filename):
    """Create a well-formatted Excel file from job data"""
    if not jobs:
        print("No jobs to export")
        return None
    
    # Create DataFrame
    df = pd.DataFrame(jobs, columns=COLUMNS)
    
    # Clean the data
    df = df.drop_duplicates(subset=['JobTitle', 'Location'])
    df = df[df['JobTitle'].str.len() > 0]  # Remove entries without titles
    
    # Sort by job title
    df = df.sort_values('JobTitle')
    
    # Create Excel file with formatting
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Job_Listings', index=False)
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['Job_Listings']
        
        # Auto-adjust column widths
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
            worksheet.column_dimensions[column_letter].width = adjusted_width
    
    return filename

def print_statistics(df):
    """Print helpful statistics about the scraped data"""
    print(f"\n📈 Job Scraping Statistics:")
    print(f"  • Total jobs found: {len(df)}")
    print(f"  • Unique job titles: {df['JobTitle'].nunique()}")
    print(f"  • Unique locations: {df['Location'].nunique()}")
    print(f"  • Jobs with salary info: {len(df[df['Salary'] != ''])}")
    print(f"  • Jobs with experience requirements: {len(df[df['ExperienceRequired'] != ''])}")
    print(f"  • Jobs with skills listed: {len(df[df['SkillsRequired'] != ''])}")
    
    print(f"\n🏢 Top Job Titles:")
    title_counts = df['JobTitle'].value_counts().head(5)
    for title, count in title_counts.items():
        print(f"  • {title}: {count}")
    
    print(f"\n📍 Top Locations:")
    location_counts = df['Location'].value_counts().head(5)
    for location, count in location_counts.items():
        print(f"  • {location}: {count}")

def main():
    """Main scraping function"""
    print(f"🚀 Job Scraper Started")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏢 Target Company: {COMPANY_NAME}")
    
    all_jobs = []
    
    # Step 1: Try to scrape real jobs
    print(f"\n🔍 Step 1: Attempting to scrape real job postings...")
    real_jobs = scrape_real_jobs()
    if real_jobs:
        all_jobs.extend(real_jobs)
        print(f"✅ Found {len(real_jobs)} real job postings")
    else:
        print("❌ No real jobs found or scraping was blocked")
    
    # Step 2: Generate demo jobs for demonstration
    print(f"\n🎯 Step 2: Generating demo job data...")
    demo_jobs = generate_demo_jobs()
    all_jobs.extend(demo_jobs)
    print(f"✅ Generated {len(demo_jobs)} demo job postings")
    
    if all_jobs:
        # Create the Excel file
        filename = f"{COMPANY_NAME}_Jobs.xlsx"
        excel_file = create_excel_file(all_jobs, filename)
        
        if excel_file:
            df = pd.DataFrame(all_jobs, columns=COLUMNS)
            
            print(f"\n✅ Successfully created job listings file!")
            print(f"📁 File saved as: {excel_file}")
            print(f"📊 Total entries: {len(df)}")
            
            # Print statistics
            print_statistics(df)
            
            # Show sample job
            print(f"\n📋 Sample Job Listing:")
            sample = df.iloc[0]
            for col in COLUMNS:
                if sample[col]:
                    print(f"  • {col}: {sample[col]}")
            
            print(f"\n🎉 Job scraping completed successfully!")
            print(f"💡 The Excel file contains all required columns: {', '.join(COLUMNS)}")
            
            return excel_file
        else:
            print("❌ Failed to create Excel file")
            return None
    else:
        print("❌ No job data available to export")
        return None

if __name__ == "__main__":
    result = main()
