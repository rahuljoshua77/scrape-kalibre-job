import csv
from requests_html import HTMLSession

# URL yang akan diambil datanya
url = "https://www.kalibrr.com/id-ID/job-board/te/QA%20engineer/1"  # Ganti dengan URL yang sesuai

# Membuat session HTML
session = HTMLSession()

# Mengirim permintaan GET ke URL
response = session.get(url)

# Membuat objek HTML dari konten response
html = response.html
 
pages = html.xpath('//li[@class="next"]/preceding-sibling::li')
last_page = pages[-1].text if pages else ''

# Kata kunci untuk filter job title

# Menyiapkan file CSV untuk menyimpan hasil
csv_filename = 'scraped_jobs.csv'
csv_file = open(csv_filename, 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Job Title', 'Company Name', 'Location', 'Posted Date', 'Apply Before', 'Job URL'])

# Set untuk melacak pekerjaan yang sudah ada
existing_jobs = set()

# Melakukan loop pada setiap item
keywords = [
    'quality assurance manual','quality assurance analyst',
    'Quality Assurance Engineer',
    'QA Tester',
    'Test Automation Engineer',
    'Software Tester',
    'Test Analyst',
    'Quality Control Inspector',
    'QA Manager',
    'Performance Testing Engineer',
    'Test Lead',
    'Test Architect','QA', 'quality assurance', 'test engineer', 'qa engineer'
]
for key in keywords:
    
    for i in range(1, int(last_page)):
        url = f"https://www.kalibrr.com/id-ID/job-board/te/{key}/{i}"  # Ganti dengan URL yang sesuai

        # Mengirim permintaan GET ke URL
        response = session.get(url)
        html = response.html
        job_items = html.xpath('//div[contains(@class,"k-grid k-border-tertiary-ghost-color k-text-sm k-p-4")]')

        for job_item in job_items:
            job_title = job_item.xpath('.//h2/a/text()')[0]
            company_name = job_item.xpath('.//div[@class="k-col-start-3 k-row-start-3 k-flex k-flex-col k-justify-end"]/span/a/text()')[0]
            location = job_item.xpath('.//div[@class="k-flex k-flex-col md:k-flex-row"]/a/text()')[0]
            dates = job_item.xpath('//*[@class="k-block k-mb-1"]/text()')[0]
            posted_job = dates.split(' • ')[0].split('Posted ')[1].split(' ago')[0]
            apply_before = dates.split(' • ')[1].split('Apply before ')[1]
            job_url = job_item.xpath('.//h2/a/@href')[0]

            # Filter job title berdasarkan kata kunci
            if any(keyword.lower() in job_title.lower() for keyword in keywords):
                # Cek apakah pekerjaan sudah ada dalam set existing_jobs
                if (job_title, company_name, location) not in existing_jobs:
                    # Menyimpan hasil ke dalam file CSV
                    csv_writer.writerow([job_title, company_name, location, posted_job, apply_before, f'https://www.kalibrr.com/{job_url}'])
                    # Tambahkan pekerjaan ke set existing_jobs
                    existing_jobs.add((job_title, company_name, location))
                    print("Job Title:", job_title)
                    print("Company Name:", company_name)
                    print("Location:", location)
                    print("Posted Date:", posted_job)
                    print('Apply before:', apply_before)
                    print("-----------------------------------")
# Menutup file CSV
csv_file.close()

# Menutup session untuk membersihkan sumber daya
session.close()

print(f"Data berhasil disimpan dalam file CSV: {csv_filename}")
