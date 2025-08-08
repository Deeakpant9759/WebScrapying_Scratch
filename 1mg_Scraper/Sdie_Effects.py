from bs4 import BeautifulSoup
import requests

class DataExtraction:
    def __init__(self, url):
        self.url = url
        self.soup = self.get_soup()

    def get_soup(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "DNT": "1",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"
        }
        page = requests.get(self.url, headers=headers)
        return BeautifulSoup(page.content, 'html.parser')

    def prescription(self):
        outer_div = self.soup.find("div", class_="DrugHeader__prescription-req___34WVy")
        if outer_div:
            span = outer_div.find("span")
            if span:
                return span.get_text(strip=True)
        return "Prescription info not found"

    def salt_compo(self):
        div_tag = self.soup.find("div", class_="saltInfo DrugHeader__meta-value___vqYM0")
        if div_tag:
            a_tag = div_tag.find("a")
            if a_tag:
                return a_tag.get_text(strip=True)
        return "Salt composition not found"

    def side_effects(self):
        side_effects_div = self.soup.find("div", id="side_effects")
        if side_effects_div:
            return side_effects_div.get_text(separator="\n", strip=True)
        return "Side effects not found"

# Usage
if __name__ == "__main__":
    URL = 'https://www.1mg.com/drugs/duolin-3-respules-3ml-480395'
    extractor = DataExtraction(URL)

    print("Prescription Required:", extractor.prescription())
    print("Salt Composition:", extractor.salt_compo())
    print("Side Effects:\n", extractor.side_effects())
