import requests
import xlwt 
from xlwt import Workbook


Base_Url = "https://fakestoreapi.com/products"
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
request_headers = {
    "User-Agent": useragent,
    "Accept-Language": "en-US,en;q=0.5"
}
def get_Data():
    response = requests.get(Base_Url,headers=request_headers)
    return response.json()
def jobs_out(data):
    wb = Workbook()
    Data_sheet = wb.add_sheet("DATA")
    headers = list(data[0].keys())
    for i in range(0,len(headers)):
        Data_sheet.write(0,i,headers[i])
    for row in range(0,len(data)):
        fake = data[row]
        values = list(fake.values())
        for col in range(len(values)):
            Data_sheet.write(row+1,col,str(values[col]))
    wb.save("fakewebstie.xls")
if __name__ == "__main__":
    fake = get_Data()
    jobs_out(fake)
    print("file saved successfyly")