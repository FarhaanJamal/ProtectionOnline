import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class PrivacyExtracter:
    def __init__(self):
        self.key_phrases = [
            r"information\s+we\s+collect",
            r"how\s+we\s+use\s+your\s+information",
            r"your\s+rights\s+and\s+choices",
            r"personal\s+information\s+we\s+collect",
            r"how\s+we\s+share\s+your\s+information",
            r"data\s+retention\s+and\s+deletion",
            r"cookies\s+and\s+similar\s+technologies",
            r"third-party\s+service\s+providers",
            r"security\s+measures",
            r"your\s+privacy\s+rights",
            r"children's\s+privacy",
            r"changes\s+to\s+this\s+privacy\s+policy"
        ]

    def extract_web_text(self, url):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text(separator=" ", strip=True)
            return text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            return None


    def find_privacy_policy(self, url):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                anchor_tags = soup.find_all('a')
                privacy_policy_urls = []
                for tag in anchor_tags:
                    if 'privacy policy' in tag.text.lower():
                        privacy_policy_urls.append(tag.get('href'))
                if not privacy_policy_urls:
                    for tag in anchor_tags:
                        if 'privacy' in tag.get('href').lower():
                            privacy_policy_urls.append(tag.get('href'))
                if not privacy_policy_urls:
                    try:
                        driver = webdriver.Chrome()
                        driver.get(url)
                        privacy_policy_links = driver.find_elements(By.TAG_NAME, 'a')
                        for link in privacy_policy_links:
                            if "privacy" in link.text.lower() or "policy" in link.text.lower():
                                privacy_policy_urls.append(link.get_attribute('href'))
                    except Exception as e:
                        print("An error occurred:", e)
                        return None
                    finally:
                        driver.quit()
                if not privacy_policy_urls:
                    print("No privacy policy found.")
                    return None
                absolute_privacy_policy_urls = [urljoin(url, u) for u in privacy_policy_urls]
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                filtered_privacy_policy_urls = [u for u in absolute_privacy_policy_urls if domain in urlparse(u).netloc]
                common_paths = ["/privacy", "/privacy-policy", "/legal/privacy"]
                verified_privacy_policy_urls = [u for u in filtered_privacy_policy_urls if any(path in u.lower() for path in common_paths)]
                final_privacy_policy_urls = []
                for policy_url in verified_privacy_policy_urls:
                    policy_content = requests.get(policy_url, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}).text.lower() 
                    if any(re.search(phrase, policy_content) for phrase in self.key_phrases):
                        final_privacy_policy_urls.append(policy_url)
                return final_privacy_policy_urls
            else:
                print(f"Error: Failed to retrieve content from {url}. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_privacy_policy_text(self, policy_url, all_url=False):
        privacy_policy_urls = self.find_privacy_policy(policy_url)
        privacy_policy_text = ""
        if privacy_policy_urls:
            for policy_url in privacy_policy_urls:
                if all_url:
                    print(policy_url)
                try:
                    response = requests.get(policy_url, headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"})
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        para_tags = soup.find_all('p')
                        for tag in para_tags:
                            privacy_policy_text += tag.text
                    else:
                        print(f"Error: Failed to retrieve content from {policy_url}. Status code: {response.status_code}")
                except Exception as e:
                    print(f"An error occurred: {e}")
        if privacy_policy_text:
            if any(re.search(phrase, privacy_policy_text) for phrase in self.key_phrases):
                return privacy_policy_text
            else:
                privacy_policy_text = None
        if not privacy_policy_text:
            try:
                options = Options()
                options.headless = True
                driver = webdriver.Chrome(options=options) 
                driver.get(policy_url)

                driver.implicitly_wait(10) 
                page_source = driver.page_source
                driver.quit()

                soup = BeautifulSoup(page_source, 'html.parser')

                privacy_policy_text = soup.get_text(separator='\n')
            except Exception as e:
                print("Error:", e)
                return None
        if privacy_policy_text:
            return privacy_policy_text
        else:
            return None


"""extractor = PrivacyExtracter()
policy_text = extractor.get_privacy_policy_text("https://openai.com/")
print(policy_text)"""
