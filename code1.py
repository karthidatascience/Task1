import re
import pandas as pd
from bs4 import BeautifulSoup
import re
from playwright.sync_api import Playwright, sync_playwright, expect
import time
rows=[]
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    for i in range(1,10):
        page.goto(f"https://www.tesco.com/groceries/en-GB/shop/treats-and-snacks/all?_gl=1*ffsgzs*_up*MQ..*_ga*MTc4MjI0MDc3OS4xNzI0Mjk4MDY3*_ga_33B19D36CY*MTcyNDI5ODA2Ny4xLjAuMTcyNDI5ODA4MC4wLjAuMTQyNTc4NjEyNw..&brand=CADBURY%2CTESCO%2CWALKERS%2CKINDER&viewAll=brand&page={i}")
        time.sleep(2)
        html_content = page.content()
        url_link = re.findall(r'https:\/\/www\.tesco\.com\/groceries\/en-GB\/products\/[\d]+', str(html_content))
        for url in url_link:
            print(url)
            context1 = browser.new_context()
            page1 = context1.new_page()
            page1.goto(url)
            time.sleep(1)
            html_content = page1.content()
            title = re.findall(
                r'component__StyledHeading-sc-1t0ixqu-0 kdSqXr ddsweb-heading styled__ProductTitle-mfe-pdp__sc-ebmhjv-6 flNJKr">[^<>]*',
                str(html_content))
            title = ' '.join(title).replace(
                'component__StyledHeading-sc-1t0ixqu-0 kdSqXr ddsweb-heading styled__ProductTitle-mfe-pdp__sc-ebmhjv-6 flNJKr">',
                '').strip()
            print(title)
            soup = BeautifulSoup(html_content, 'html.parser')
            image_tag = soup.find('img', id='carousel__product-image')
            image_ = []
            if image_tag:
                image_src = image_tag['src']
                image_.append(image_src)
            else:
                image_src1 = 'not found image'
                image_.append(image_src1)

            image = ' '.join(image_)
            print(image)

            price1 = re.findall(
                r'text__StyledText-sc-1jpzi8m-0 lmgzsH ddsweb-text styled__PriceText-sc-v0qv7n-1 eNIEDh">[^<>]*', str(soup))
            price1 = ' '.join(price1).replace(
                'text__StyledText-sc-1jpzi8m-0 lmgzsH ddsweb-text styled__PriceText-sc-v0qv7n-1 eNIEDh">',
                '').strip()
            # print(price1)

            price2 = re.findall(
                r'text__StyledText-sc-1jpzi8m-0 dyJCjQ ddsweb-text styled__Subtext-sc-v0qv7n-2 nsITR ddsweb-price__subtext">[^<>]*',
                str(soup))
            price2 = ' '.join(price2).replace(
                'text__StyledText-sc-1jpzi8m-0 dyJCjQ ddsweb-text styled__Subtext-sc-v0qv7n-2 nsITR ddsweb-price__subtext">',
                '').strip()
            # print(price2)
            price = price1 + " " + price2
            print(price)
            availablity='In Stock'

            s1 = soup.find_all('div', class_='styled__PanelContent-sc-110ics9-5 eCnSbU')[1]
            # print(s1)
            nutrifields = []
            for row in s1.find_all('tr'):  # Loop through each row
                columns = row.find_all(['th', 'td'])  # Use 'th' for header cells
                row_data = [column.text for column in columns]
                nutrifields.append(row_data)
            print(nutrifields)
            row_dict = {
                'url': url,
                'title': title,
                'image': image,
                'price': price,
                'availablity':availablity,
                'nutrifields': nutrifields,
            }
            rows.append(row_dict)

            result_df = pd.DataFrame(rows)
            result_df.to_excel('tesco.xlsx', index=False)


            context1.close()

        context.close()
        browser.close()


with sync_playwright() as playwright:
    run(playwright)


