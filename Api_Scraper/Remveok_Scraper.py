import requests
import xlwt
from xlwt import Workbook

# Constants
base_url = "https://remoteok.com/api/"
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
request_headers = {
    "User-Agent": useragent,
    "Accept-Language": "en-US,en;q=0.5"
}

# Get job data from RemoteOK API
def get_jobs():
    response = requests.get(base_url, headers=request_headers)
    return response.json()

# Write job data to Excel
def output_job_Excel(data):
    wb = Workbook()
    job_sheet = wb.add_sheet("Jobs")

    # Write headers
    headers = list(data[0].keys())
    for i in range(len(headers)):
        job_sheet.write(0, i, headers[i])

    for row in range(0,len(data)):
        job = data[row]
        values = list(job.values())
        for col in range(len(values)):
            job_sheet.write(row + 1, col, values[col])

    # Save the file
    wb.save("RemoteOK_Jobs.xls")

# Main function
if __name__ == "__main__":
    jobs = get_jobs()[1:]  # Skipping the first me  tadata entry
    output_job_Excel(jobs)
    print("Job data has been written to RemoteOK_Jobs.xls")
