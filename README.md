# Website-Crawler-and-PDF-Generator

## Overview
This Python script is a powerful web crawling tool that allows you to scrape website content and generate a comprehensive PDF document of the crawled pages. It provides a flexible way to extract and preserve web content from a given website.

![image](https://github.com/user-attachments/assets/3e4d6b75-cd12-420e-9139-59e024fa3f9a)


## Features
- Crawl websites with customizable depth and page limits
- Extract clean text content from web pages
- Ignore non-text files and resources
- Generate a PDF with source URLs and extracted content
- User-friendly command-line interface

## Prerequisites
Before running the script, ensure you have the following dependencies installed:
- Python 3.7+
- Required Python libraries:
    - requests
    - beautifulsoup4
    - reportlab

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/website-crawler.git
cd website-crawler
```

2. Install the required dependencies:
```bash
pip install requests beautifulsoup4 reportlab
```

## Usage
Run the script from the command line:
```bash
python website_crawler.py
```

When prompted, provide:
- The base URL of the website you want to crawl
- Maximum number of pages to crawl (default: 50)
- Maximum link depth to follow (default: 3)

## Example
```
Enter the homepage URL to crawl and convert to PDF: https://example.com
Maximum number of pages to crawl (default 50): 30
Maximum link depth to follow (default 3): 
```

The script will:
1. Crawl the specified website
2. Extract text content from each page
3. Generate a PDF with the extracted content
4. Save the PDF with a filename based on the website domain

## Customization
You can modify the ```WebsiteCrawler``` class to:
- Change excluded file extensions
- Adjust crawling and extraction behavior
- Add more sophisticated text processing

## Limitations
- Only crawls websites within the same domain
- Skips binary and non-text files
- Respects a simple rate limit (1-second delay between requests)

## Dependencies
- ```os```: File and path operations
- ```requests```: HTTP requests
- ```BeautifulSoup```: HTML parsing
- ```reportlab```: PDF generation
- ```urllib.parse```: URL handling
- ```re```: Regular expression operations
- ```time```: Crawl rate limiting

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
Licensed under the MIT License - see MIT License for details.

>[!NOTE]
This tool is for educational and research purposes. Always respect website terms of service and robots.txt guidelines when crawling websites.
