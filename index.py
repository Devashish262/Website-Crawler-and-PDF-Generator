import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re
import time

class WebsiteCrawler:
    def __init__(self, base_url, max_pages=50, max_depth=3):
        """
        Initialize the website crawler
        
        :param base_url: Starting URL of the website
        :param max_pages: Maximum number of pages to crawl
        :param max_depth: Maximum depth of links to follow
        """
        self.base_url = base_url
        self.max_pages = max_pages
        self.max_depth = max_depth
        
        self.parsed_base_url = urlparse(base_url)

        self.crawled_urls = set()
        self.urls_to_crawl = [(base_url, 0)]
        
        self.page_contents = []

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def is_valid_url(self, url):
        """
        Check if URL is valid and within the same domain
        
        :param url: URL to validate
        :return: Boolean indicating if URL is valid
        """
        parsed_url = urlparse(url)
        
        domain_match = parsed_url.netloc == self.parsed_base_url.netloc
        
        excluded_extensions = [
            '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.mp3', 
            '.mp4', '.zip', '.rar', '.exe', '.css', '.js'
        ]
        file_excluded = not any(url.lower().endswith(ext) for ext in excluded_extensions)
        
        return domain_match and file_excluded

    def extract_text(self, html_content):
        """
        Extract clean text from HTML content
        
        :param html_content: Raw HTML content
        :return: Cleaned text content
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        for script in soup(["script", "style", "nav", "header", "footer", "iframe", "form"]):
            script.decompose()
        
        text = soup.get_text(separator=' ', strip=True)
        
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def crawl(self):
        """
        Crawl the website and collect page contents
        """
        while self.urls_to_crawl and len(self.crawled_urls) < self.max_pages:
            current_url, depth = self.urls_to_crawl.pop(0)
            
            if current_url in self.crawled_urls or depth > self.max_depth:
                continue
            
            try:
                response = requests.get(current_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                text_content = self.extract_text(response.text)
                
                if text_content:
                    self.page_contents.append({
                        'url': current_url,
                        'content': text_content
                    })
                
                self.crawled_urls.add(current_url)
                
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    absolute_url = urljoin(current_url, link['href'])
                    
                    if (self.is_valid_url(absolute_url) and 
                        absolute_url not in self.crawled_urls and 
                        absolute_url not in [url for url, _ in self.urls_to_crawl]):
                        self.urls_to_crawl.append((absolute_url, depth + 1))
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Error crawling {current_url}: {e}")

    def generate_pdf(self, output_filename=None):
        """
        Generate a PDF from collected website contents
        
        :param output_filename: Custom PDF filename
        """

        if not output_filename:
            parsed_url = urlparse(self.base_url)
            output_filename = f"{parsed_url.netloc}_website_content.pdf"
        
        if not output_filename.lower().endswith('.pdf'):
            output_filename += '.pdf'
        
        pdf = SimpleDocTemplate(output_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        url_style = ParagraphStyle(
            'URLStyle',
            parent=styles['Heading2'],
            textColor='blue',
            fontSize=10
        )
        
        elements = []
        
        for page in self.page_contents:
            url_para = Paragraph(f"Source: {page['url']}", url_style)
            elements.append(url_para)
            
            paragraphs = page['content'].split('. ')
            for para_text in paragraphs:
                if para_text.strip():
                    para = Paragraph(para_text + '.', styles['Normal'])
                    elements.append(para)
                    elements.append(Spacer(1, 0.25*inch))

        try:
            pdf.build(elements)
            print(f"PDF created successfully: {output_filename}")
        except Exception as e:
            print(f"Error creating PDF: {e}")

def main():
    base_url = input("Enter the homepage URL to crawl and convert to PDF: ").strip()
    
    try:
        max_pages = int(input("Maximum number of pages to crawl (default 50): ") or 50)
        max_depth = int(input("Maximum link depth to follow (default 3): ") or 3)
    except ValueError:
        print("Invalid input. Using default values.")
        max_pages, max_depth = 50, 3
    
    crawler = WebsiteCrawler(base_url, max_pages, max_depth)
    
    print("Starting website crawl...")
    crawler.crawl()
    
    print(f"Crawled {len(crawler.crawled_urls)} pages. Generating PDF...")
    crawler.generate_pdf()

if __name__ == "__main__":
    main()
