import json
import requests
import pandas as pd
import time
from bs4 import BeautifulSoup
from openpyxl import Workbook, load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font, PatternFill
from datetime import datetime
import os

class BulkDataExtraction:
    def __init__(self, csv_file_path, output_file="bulk_drug_data.xlsx"):
        self.csv_file_path = csv_file_path
        self.output_file = output_file
        self.processed_count = 0
        self.failed_urls = []
        
    def get_soup(self, url):
        """Get soup object for a URL with error handling"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                "Accept-Encoding": "gzip, deflate",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "DNT": "1",
                "Connection": "close",
                "Upgrade-Insecure-Requests": "1"
            }
            page = requests.get(url, headers=headers, timeout=30)
            page.raise_for_status()
            return BeautifulSoup(page.content, 'html.parser')
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {str(e)}")
            return None

    def extract_single_url_data(self, url):
        """Extract all data for a single URL"""
        soup = self.get_soup(url)
        if not soup:
            return None
            
        try:
            data = {
                'url': url,
                'prescription': self.prescription(soup),
                'salt_composition': self.salt_compo(soup),
                'side_effects': self.side_effects(soup),
                'product_description': self.product_description(soup),
                'faqs': self.format_faqs_for_excel(self.faqs(soup)),
                'how_drug_works': self.format_how_drug_works_for_excel(self.how_drug_works(soup)),
                'drug_interactions': self.format_drug_interactions_for_excel(self.drug_interaction(soup)),
                'how_to_use': self.format_how_to_use_for_excel(self.how_to_use(soup)),
                'safety_advice': self.format_safety_advice_for_excel(self.safety_advice(soup))
            }
            return data
        except Exception as e:
            print(f"❌ Error extracting data from {url}: {str(e)}")
            return None

    def prescription(self, soup):
        outer_div = soup.find("div", class_="DrugHeader__prescription-req___34WVy")
        if outer_div:
            span = outer_div.find("span")
            if span:
                return span.get_text(strip=True)
        return ""

    def salt_compo(self, soup):
        div_tag = soup.find("div", class_="saltInfo DrugHeader__meta-value___vqYM0")
        if div_tag:
            a_tag = div_tag.find("a")
            if a_tag:
                return a_tag.get_text(strip=True)
        return ""

    def side_effects(self, soup):
        side_effects_div = soup.find("div", id="side_effects")
        if side_effects_div:
            return side_effects_div.get_text(separator="\n", strip=True)
        return ""

    def product_description(self, soup):
        product_intro_div = soup.find("div", class_="DrugOverview__container___CqA8x")
        if product_intro_div:
            return product_intro_div.get_text(separator=" ", strip=True)
        return ""

    def faqs(self, soup):
        faq_div = soup.find("div", id="faq")
        faq_list = []
        if faq_div:
            for tile in faq_div.find_all("div", class_="Faqs__tile___1B58W"):
                question_tag = tile.find("h3", class_="Faqs__ques___1iPB9")
                answer_tag = tile.find("div", class_="Faqs__ans___1uuIW")
                if question_tag and answer_tag:
                    faq_list.append({
                        "Q": question_tag.get_text(strip=True),
                        "A": answer_tag.get_text(strip=True)
                    })
        return faq_list

    def how_drug_works(self, soup):
        container = soup.find("div", id="how_drug_works")
        if container:
            title_tag = container.find("h2")
            content_tag = container.find("div", class_="DrugOverview__content___22ZBX")
            title = title_tag.get_text(strip=True) if title_tag else ""
            content = content_tag.get_text(strip=True) if content_tag else ""
            return {"title": title, "content": content}
        return {}

    def drug_interaction(self, soup):
        interaction_div = soup.find("div", id="drug_interaction")
        if interaction_div:
            title_tag = interaction_div.find("h2")
            description_tag = interaction_div.find("div", class_="DrugInteraction__desc___2y8bR")
            title = title_tag.get_text(strip=True) if title_tag else ""
            description = description_tag.get_text(strip=True) if description_tag else ""

            interactions = []
            for drug_block in interaction_div.find_all("div", class_="DrugInteraction__drug___1XyzI"):
                name = drug_block.get_text(strip=True)
                desc_block = drug_block.find_next("div", class_="DrugInteraction__interaction-text___1hOwx")
                desc_text = desc_block.get_text(" ", strip=True) if desc_block else ""
                interactions.append({"drug": name, "description": desc_text})

            return {
                "title": title,
                "description": description,
                "interactions": interactions
            }
        return {}

    def how_to_use(self, soup):
        how_to_use_div = soup.find("div", id="how_to_use")
        if how_to_use_div:
            heading_tag = how_to_use_div.find("h2")
            instructions_tag = how_to_use_div.find("div", class_="DrugOverview__content___22ZBX")
            heading = heading_tag.get_text(strip=True) if heading_tag else ""
            instructions = instructions_tag.get_text(" ", strip=True) if instructions_tag else ""
            return {"heading": heading, "instructions": instructions}
        return {}

    def safety_advice(self, soup):
        safety_div = soup.find("div", id="safety_advice")
        if not safety_div:
            return {}

        heading_tag = safety_div.find("h2")
        heading = heading_tag.get_text(strip=True) if heading_tag else ""

        safety_items = []
        warnings = safety_div.find_all("div", class_="DrugOverview__warning-top___UD3xX")

        for warning in warnings:
            label_tag = warning.find("span")
            status_tag = warning.find("div", class_="DrugOverview__warning-tag___aHZlc")

            label = label_tag.get_text(strip=True) if label_tag else ""
            status = status_tag.get_text(strip=True) if status_tag else ""

            desc_div = warning.find_next_sibling("div", class_="DrugOverview__content___22ZBX")
            description = desc_div.get_text(" ", strip=True) if desc_div else ""

            safety_items.append({
                "label": label,
                "status": status,
                "description": description
            })

        return {"heading": heading, "items": safety_items}

    def format_faqs_for_excel(self, faqs):
        if not faqs:
            return ""
        formatted_text = ""
        for i, faq in enumerate(faqs, 1):
            formatted_text += f"Q{i}: {faq['Q']}\n"
            formatted_text += f"A{i}: {faq['A']}\n\n"
        return formatted_text.strip()

    def format_drug_interactions_for_excel(self, interactions_data):
        if not interactions_data:
            return ""
        formatted_text = ""
        if interactions_data.get('title'):
            formatted_text += f"TITLE: {interactions_data['title']}\n\n"
        if interactions_data.get('description'):
            formatted_text += f"DESCRIPTION: {interactions_data['description']}\n\n"
        if interactions_data.get('interactions'):
            formatted_text += "DRUG INTERACTIONS:\n"
            for i, interaction in enumerate(interactions_data['interactions'], 1):
                formatted_text += f"{i}. {interaction['drug']}\n"
                formatted_text += f"   Description: {interaction['description']}\n\n"
        return formatted_text.strip()

    def format_safety_advice_for_excel(self, safety_data):
        if not safety_data:
            return ""
        formatted_text = ""
        if safety_data.get('heading'):
            formatted_text += f"HEADING: {safety_data['heading']}\n\n"
        if safety_data.get('items'):
            for i, item in enumerate(safety_data['items'], 1):
                formatted_text += f"{i}. {item['label']}\n"
                formatted_text += f"   Status: {item['status']}\n"
                formatted_text += f"   Description: {item['description']}\n\n"
        return formatted_text.strip()

    def format_how_drug_works_for_excel(self, how_works_data):
        if not how_works_data:
            return ""
        formatted_text = ""
        if how_works_data.get('title'):
            formatted_text += f"TITLE: {how_works_data['title']}\n\n"
        if how_works_data.get('content'):
            formatted_text += f"CONTENT: {how_works_data['content']}"
        return formatted_text.strip()

    def format_how_to_use_for_excel(self, how_to_use_data):
        if not how_to_use_data:
            return ""
        formatted_text = ""
        if how_to_use_data.get('heading'):
            formatted_text += f"HEADING: {how_to_use_data['heading']}\n\n"
        if how_to_use_data.get('instructions'):
            formatted_text += f"INSTRUCTIONS: {how_to_use_data['instructions']}"
        return formatted_text.strip()

    def create_excel_with_headers(self):
        """Create Excel file with headers if it doesn't exist"""
        if os.path.exists(self.output_file):
            return
            
        wb = Workbook()
        ws = wb.active
        ws.title = "Drug Data"

        # Headers - URL as first column
        headers = [
            "URL",
            "Prescription Required",
            "Salt Composition", 
            "Side Effects",
            "Product Description",
            "FAQs",
            "How Drug Works",
            "Drug Interactions",
            "How to Use",
            "Safety Advice"
        ]
        
        ws.append(headers)
        
        # Format headers
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal="center", vertical="center")

        # Set column widths
        column_widths = [50, 20, 30, 40, 60, 60, 60, 60, 60, 60]
        for i, width in enumerate(column_widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = width

        wb.save(self.output_file)
        print(f"✅ Created Excel file: {self.output_file}")

    def append_data_to_excel(self, data_batch):
        """Append batch of data to existing Excel file"""
        try:
            wb = load_workbook(self.output_file)
            ws = wb.active
            
            for data in data_batch:
                if data:  # Only add if data extraction was successful
                    row_data = [
                        data['url'],
                        data['prescription'],
                        data['salt_composition'],
                        data['side_effects'],
                        data['product_description'],
                        data['faqs'],
                        data['how_drug_works'],
                        data['drug_interactions'],
                        data['how_to_use'],
                        data['safety_advice']
                    ]
                    ws.append(row_data)
                    
                    # Format the new row
                    row_num = ws.max_row
                    for cell in ws[row_num]:
                        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
                    ws.row_dimensions[row_num].height = 100
            
            wb.save(self.output_file)
            print(f"✅ Saved batch to Excel. Total rows: {ws.max_row - 1}")
            
        except Exception as e:
            print(f"❌ Error saving to Excel: {str(e)}")

    def process_urls_from_csv(self, start_from=0, has_header=False):
        """Main method to process URLs from CSV with breaks"""
        
        # Read CSV file
        try:
            if has_header:
                df = pd.read_csv(self.csv_file_path)
                print(f"📊 Loaded {len(df)} URLs from CSV (with header)")
                
                # Detect URL column (assuming first column or column named 'url', 'URL', 'urls', etc.)
                url_column = None
                possible_url_columns = ['url', 'URL', 'urls', 'URLs', 'link', 'links']
                
                for col in possible_url_columns:
                    if col in df.columns:
                        url_column = col
                        break
                
                if url_column is None:
                    url_column = df.columns[0]  # Use first column as default
                    
                urls = df[url_column].tolist()
                print(f"🔗 Using column '{url_column}' for URLs")
                
            else:
                # Read CSV without header - data starts from index 0
                df = pd.read_csv(self.csv_file_path, header=None)
                print(f"📊 Loaded {len(df)} URLs from CSV (no header - data starts from index 0)")
                
                # Use first column (index 0) for URLs
                urls = df[0].tolist()
                print(f"🔗 Using first column for URLs (no header detected)")
            
        except Exception as e:
            print(f"❌ Error reading CSV: {str(e)}")
            return

        # Create Excel file with headers
        self.create_excel_with_headers()
        
        # Start processing from specified index
        urls = urls[start_from:]
        total_urls = len(urls)
        print(f"🚀 Starting to process {total_urls} URLs...")
        
        batch_data = []
        
        for i, url in enumerate(urls):
            current_index = start_from + i + 1
            
            print(f"🔄 Processing URL {current_index}/{start_from + total_urls}: {url}")
            
            # Extract data for this URL
            data = self.extract_single_url_data(url)
            
            if data:
                batch_data.append(data)
                self.processed_count += 1
            else:
                self.failed_urls.append(url)
            
            # Save every 30 URLs and take 3 second break
            if current_index % 30 == 0:
                if batch_data:
                    self.append_data_to_excel(batch_data)
                    batch_data = []
                
                print("⏸️ Taking 3 second break after 30 URLs...")
                time.sleep(3)
            
            # Take 5 minute break every 10k URLs
            if current_index % 10000 == 0:
                print(f"🕐 Processed {current_index} URLs. Taking 5 minute break...")
                print(f"📈 Success rate: {self.processed_count}/{current_index} ({(self.processed_count/current_index)*100:.1f}%)")
                time.sleep(300)  # 5 minutes = 300 seconds
                
        # Save any remaining data
        if batch_data:
            self.append_data_to_excel(batch_data)
            
        # Print final statistics
        print("\n" + "="*50)
        print("🎉 PROCESSING COMPLETE!")
        print(f"📊 Total URLs processed: {self.processed_count}")
        print(f"❌ Failed URLs: {len(self.failed_urls)}")
        print(f"✅ Success rate: {(self.processed_count/(self.processed_count + len(self.failed_urls)))*100:.1f}%")
        print(f"💾 Data saved to: {self.output_file}")
        
        # Save failed URLs to a separate file
        if self.failed_urls:
            failed_df = pd.DataFrame(self.failed_urls, columns=['failed_urls'])
            failed_file = f"failed_urls_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            failed_df.to_csv(failed_file, index=False)
            print(f"📝 Failed URLs saved to: {failed_file}")


# Usage
if __name__ == "__main__":
    # Initialize the bulk processor
    csv_file = r"C:\Users\MICILMEDS\Battel_with_Codes\WebScrapying_Scratch\URL.csv"
    
    bulk_extractor = BulkDataExtraction(
        csv_file_path=csv_file,
        output_file="bulk_drug_data.xlsx"
    )
    
    # Start processing - CSV has no header, data starts from index 0
    bulk_extractor.process_urls_from_csv(start_from=0, has_header=False)
    # If your CSV had headers, you would use:
    # bulk_extractor.process_urls_from_csv(start_from=0, has_header=True)