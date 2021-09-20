import csv
import time
import requests
from bs4 import BeautifulSoup

with open('1k-cities-pwd.csv', 'r') as f:
    reader = csv.reader(f)
    queue = 1 
    total_emails = 0
    for row in reader:
        print()
        start = time.time()
        emails = []
        city = row[0]
        state = row[1]
        URL = row[2]
        print(city + ", " + state + " (" + str(queue) + " of 13454)")
        print("Searching " + URL)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        mailtos = soup.select('a[href^=mailto]')
        for i in mailtos:
            href=i['href']
            try:
                str1, str2 = href.split(':')
            except ValueError:
                break
            emails.append(str2)
        email_string = ';'.join(emails)
        if len(emails) > 0:
            for email in emails:
                print(email)
        total_emails = total_emails + len(emails)
        print("Found Emails: " + str(len(emails)))
        print('\033[1m' + "TOTAL EMAILS: "+ str(total_emails) + '\033[0m')
        queue += 1
        time.sleep(1)
        data = [city, state, email_string]
        with open('1k-cities-emails.csv', 'a') as e:
            writer = csv.writer(e)
            writer.writerow(data)
        