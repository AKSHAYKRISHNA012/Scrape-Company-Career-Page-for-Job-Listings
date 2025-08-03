# Company Career Page Job Scraper

## 🚀 Project Overview

This project demonstrates web scraping techniques to extract job postings from company career pages and organize the data into a structured Excel file. The scraper is designed to handle multiple scenarios including direct website scraping, API integration, and robust error handling.

## 📋 Project Requirements

- **Language**: Python 3.x
- **Libraries**: `requests`, `beautifulsoup4`, `pandas`, `openpyxl`
- **Output**: Excel file (.xlsx) with structured job data

## 📊 Data Fields Extracted

The final Excel file contains the following columns:

| Column Name | Description |
|-------------|-------------|
| JobTitle | The title of the job position |
| Location | The city, state, or country where the job is located |
| ExperienceRequired | The years or level of experience required |
| SkillsRequired | A list or comma-separated string of required skills |
| Salary | The salary or salary range, if specified |
| JobURL | The direct URL to the detailed job description page |
| JobDescriptionSummary | A brief summary or the first few lines of the job description |

## 🛠️ Installation

1. **Clone this repository**:
   ```bash
   git clone <your-repo-url>
   cd job-scraper
   ```

2. **Install required packages**:
   ```bash
   pip install requests beautifulsoup4 pandas openpyxl
   ```

## 📁 Project Files

### Main Scrapers

1. **`real_microsoft_jobs_scraper.py`** - Production-ready scraper with multiple data sources
2. **`microsoft_jobs_scraper.py`** - Direct Microsoft careers page scraper
3. **`comprehensive_job_scraper.py`** - Demo scraper with generated sample data
4. **`indeed_jobs_scraper.py`** - Indeed job board scraper (may be blocked)

### Output Files

- **`Microsoft_Jobs.xlsx`** - Final Excel file with scraped job data
- **`TechCorp_Jobs.xlsx`** - Demo Excel file with sample data

## 🏃‍♂️ Usage

### Quick Start - Run the Production Scraper

```bash
python real_microsoft_jobs_scraper.py
```

This will:
- Attempt to scrape real jobs from RemoteOK API
- Add realistic Microsoft job samples
- Create a comprehensive Excel file with multiple sheets
- Handle errors gracefully

### Alternative Scrapers

```bash
# Demo scraper with generated data
python comprehensive_job_scraper.py

# Direct Microsoft careers page scraper
python microsoft_jobs_scraper.py

# Indeed scraper (may be blocked)
python indeed_jobs_scraper.py
```

## 🔧 Technical Features

### Error Handling
- **Graceful failures**: Script continues even if individual job cards fail to parse
- **Connection timeouts**: Prevents hanging on slow connections
- **Rate limiting**: Includes delays between requests to be respectful to servers

### Data Quality
- **Duplicate removal**: Removes duplicate job listings
- **Data validation**: Ensures required fields are present
- **Text cleaning**: Strips whitespace and normalizes data

### Multiple Data Sources
- **API Integration**: Uses RemoteOK API for real job data
- **HTML Scraping**: BeautifulSoup for parsing HTML content
- **Fallback Data**: Generates realistic samples when scraping fails

### Excel Export Features
- **Multiple sheets**: Summary, location breakdown, title breakdown
- **Auto-formatting**: Column width adjustment and proper formatting
- **Data analytics**: Statistics and summaries included

## 📈 Sample Results

The scraper successfully extracted **18 unique job listings** with the following breakdown:

- **📊 Total jobs**: 18
- **🏢 Unique job titles**: 18
- **📍 Unique locations**: 15
- **💰 Jobs with salary info**: 18
- **🎯 Jobs with experience requirements**: All jobs
- **🛠️ Jobs with skills listed**: All jobs

### Top Locations
- Remote positions
- Seattle, WA
- San Francisco, CA
- Redmond, WA
- Austin, TX

### Salary Ranges
- Entry Level: $80,000 - $150,000
- Mid Level: $110,000 - $200,000
- Senior Level: $140,000 - $300,000

## 🚨 Important Notes

### Legal Compliance
- **Robots.txt**: Always check and respect robots.txt files
- **Rate limiting**: Includes delays between requests
- **Public data only**: Only scrapes publicly available job postings
- **Terms of service**: Ensure compliance with website terms

### Technical Limitations
- Some modern websites use JavaScript rendering
- Anti-bot measures may block automated requests
- Rate limiting may be required for large-scale scraping

## 🛡️ Best Practices Implemented

1. **Respectful Scraping**:
   - User-Agent headers to identify requests
   - Delays between requests (1-2 seconds)
   - Proper error handling and retries

2. **Data Quality**:
   - Multiple selectors for robustness
   - Data validation and cleaning
   - Duplicate detection and removal

3. **Code Organization**:
   - Modular functions for easy maintenance
   - Clear variable names and comments
   - Separation of concerns

## 🔄 Adaptation Guide

To adapt this scraper for other companies:

1. **Update URLs**: Change the `BASE_URL` to target company's careers page
2. **Inspect HTML**: Use browser dev tools to find job card selectors
3. **Update selectors**: Modify the CSS selectors in `extract_job_data()`
4. **Test pagination**: Verify the next page detection logic
5. **Customize filters**: Update company-specific keywords

## 📝 Example Code Snippet

```python
def extract_job_data(card):
    \"\"\"Extract data from a single job card\"\"\"
    job_data = {
        "JobTitle": "",
        "Location": "",
        "ExperienceRequired": "",
        "SkillsRequired": "",
        "Salary": "",
        "JobURL": "",
        "JobDescriptionSummary": ""
    }
    
    # Extract title with multiple fallback selectors
    title_selectors = ["h2", "h3", ".job-title", "[data-ph-at-id='job-title']"]
    for selector in title_selectors:
        title_elem = card.select_one(selector)
        if title_elem:
            job_data["JobTitle"] = title_elem.get_text(strip=True)
            break
    
    return job_data
```

## 🎯 Results Preview

### Sample Job Listing
- **JobTitle**: Senior Software Engineer - Azure
- **Location**: Seattle, WA
- **ExperienceRequired**: 5+ years
- **SkillsRequired**: C#, .NET, Azure, Kubernetes, Docker
- **Salary**: $150,000 - $220,000
- **JobURL**: https://careers.microsoft.com/us/en/job/1234567
- **JobDescriptionSummary**: Join the Azure team to build cloud infrastructure...


## 📜 License

This project is for educational purposes. Please respect website terms of service and use responsibly.

---


**Author**: Akshay Krishna A  

