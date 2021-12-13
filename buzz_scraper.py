import requests
import bs4

"""
csv file structure:
link1,price_threshold1
link2,price_threshold2
...

-------------------
email must be gmail
-------------------
website: https://www.buzzsneakers.com/RON_ro
"""

FILE_PATH = f'G:\\bs-buzzsneakers\\products.csv'
EMAIL_ADDRESS = ""
PASSWORD = ""

# TODO: validation for from_ to be email
def send_mail(from_, to, password, my_list):
    import smtplib
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_, password)
    
    msg = "Subject: To buy: buzz\n\n"
    for item in my_list:
        msg += item
        msg += "\n"
        
    server.sendmail(from_, to, msg)
    server.quit()
    print("mail sent")

    
def csv_to_dict(file_name):
    import csv
    
    reader = csv.reader(open(file_name, 'r'))
    dict = {}
    for row in reader:
        k, v = row
        dict[k] = v
    
    return dict

def modify_csv(filename, index_list):
    import pandas as pd
    
    df = pd.read_csv(filename, encoding='utf-8', header=None)
    
    df = df.drop(index_list)

    df.to_csv(filename, encoding='utf-8', header=None, index=False)


def main():
    print("starting buzz scraper")
    tobuy_list = []
    dict = csv_to_dict(FILE_PATH) # values are strings...
    
    for link in dict:
        res = requests.get(f'{link}')
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        
        price = soup.find('span',{'class':'product-price-value value'}).get_text().strip()
        price = float(price.replace(",", "."))  # cast from string
        if price <= float(dict[link]):
            tobuy_list.append(link)
    
    dlist = list(dict)
    index_list = []
    for prod in dlist:
        if prod in tobuy_list:
            index_list.append(dlist.index(prod))
            
    if tobuy_list:
        send_mail(EMAIL_ADDRESS, EMAIL_ADDRESS, PASSWORD, tobuy_list)        
        modify_csv(FILE_PATH, index_list)
        print("Found something, check your email!")
        
    print("Done scraping")
    

if __name__ == "__main__":
    main()
    