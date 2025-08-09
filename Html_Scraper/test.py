import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent



ua = UserAgent()
request_headers = {"User-Agent": ua.random}



def get_page_html(url):
    res = requests.get(url=url,headers=request_headers)
    return res.content

def get_product_price(soup):
    # Price (full, with ₹)
    container = soup.find('div',class_ = 'a-section a-spacing-none aok-align-center aok-relative')
    if container:
        target_span = container.find('span',class_='aok-offscreen')
        if target_span:
            text_value = target_span.get_text(strip=True)
            return text_value
    

def extract_product_info(url):
    product_info={}
    print(f"Extract the data of {url}")
    html = get_page_html(url=url)
    soup = BeautifulSoup(html,'html.parser')
    product_info['Price'] = get_product_price(soup)
    return product_info



if __name__ == "__main__":
    #with open(r"C:\Users\MICILMEDS\Battel_with_Codes\WebScrapying_Scratch\Html_Scraper\Amazon_products.csv",newline='') as csvfile:
        #reader = csv.reader(csvfile,delimiter=",")
        #for rw in reader:
            url = 'https://www.amazon.in/Redmi-Note-14-5G-Dimensity/dp/B0DPFTYQN7/ref=sr_1_1_sspa?crid=3GMG52BTVYP0G&dib=eyJ2IjoiMSJ9.WFxCmg4fW900Jb-ghJ-WzcqbOex1V1yH1ZD5sgNjt2f5tkhHACiJI2VV-eC2EW4KtAe-P7E03QAvt09KwC6KFnxygo8GD-au57hsFnQ2ytrHGcz3GJsHf71FJlcD9Moa9KTBfmnm7OktC80tO__98F5_7EZcLTjR7cyAnLxUgB7GopRsiwrv3SmkW3RyNmIQW8Ys4DtpCKY_aEhOXiyD_6o5l0sp5A1FYu2MvXp_BXI.vVHuptBpdjbovg59qjcyRrzF9SKwZ5grgHvQhm1jXJQ&dib_tag=se&keywords=best%2Bphone%2Bunder%2B20k&qid=1754729718&sprefix=best%2Bphone%2B%2Caps%2C229&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1'
            print(extract_product_info(url))