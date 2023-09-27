import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
# from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager



name = input('Tovarni kiriting: ')
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()), 
    # options=Options()
  )
driver.get(f"https://uzum.uz/uz/search?query={name}&needsCorrection=1&sorting=orders&ordering=descending&currentPage=1")



driver.maximize_window()

time.sleep(13)

html = driver.page_source

soup = BeautifulSoup(html, features="lxml")
products = soup.find('div', attrs={"data-test-id": "list__products"})
products = products.find_all('div', class_="col-mbs-12 col-mbm-6 col-xs-4 col-md-3")
# print(products, '\n\n\n\n')
# print(len(products))

def filter_products(product_list):
    filtered_products = []
    for product in product_list:
        if product["product_price"] > 1000000:
            filtered_products.append(product)
    if len(filtered_products) == 0:
        filtered_products = product_list
    return filtered_products

def choose_best_product(product_list):
    best_product = None
    best_score = 0

    for product in product_list:
        score = (product["product_rating"] * int(product["product_rating_count"])) / product["product_price"]
        if score > best_score or best_product is None:
            best_product = product
            best_score = score

    return best_product


products_list = []

for product in products:
  product_link = product.find('a', attrs={"ui-link": "ui-link"}).get('href')
  product_price = product.find('span', attrs={"data-test-id": "text__price"}).text.strip()
  # print(product.find('span', attrs={"data-test-id": "text__rating"}))
  print(product.find('span', attrs={"data-test-id": "text__orders"}))
  
  if product.find('span', attrs={"data-test-id": "text__rating"}) != None:
    product_rating = float(product.find('span', attrs={"data-test-id": "text__rating"}).text.strip())  
  else: product_rating=1
    
  if product.find('span', attrs={"data-test-id": "text__orders"}) != None:
    product_rating_count = str(''.join(filter(str.isdigit, product.find('span', attrs={"data-test-id": "text__orders"}).text.strip())))[2:]
    if len(product_rating_count) == 0: product_rating_count=1
  else: product_rating_count=1


  products_list.append({
    'product_price': int(''.join(filter(str.isdigit, product_price))),
    'product_link': f"https://uzum.uz/uz{product_link}",
    'product_rating_count': product_rating_count,
    'product_rating': product_rating
  })



with open('products.json', 'w', encoding='utf-8') as f:
  json.dump(products_list, f, ensure_ascii=False, indent=2)
  # f.write(str(products))
  f.close()

products_list = filter_products(products_list)

best_product = choose_best_product(products_list)

if best_product:
    print("Link:", best_product["product_link"])
else:
    print("None")

# pagination = soup.find('ul', class_='pagination')

# for i in pagination.find_all('li'):
#   print(i.text)



# revealed = driver.find_element(By.CSS_SELECTOR, "#main-page > div > header > div:nth-child(1) > div.middle-header.row.center.between-mbs.middle-mbs.noselect > div.store-action-buttons > div").click()

# wait = WebDriverWait(driver, timeout=10)

# wait.until(lambda d : revealed.is_displayed())
# revealed.send_keys("Displayed")

# time.sleep(10)
# savatcha1 = driver.find_element(
#     By.CSS_SELECTOR, "div.home-products:nth-child(5) > div:nth-child(1) > div:nth-child(1) > h2:nth-child(1)")
# savatcha1 = driver.find_element(
#     By.CSS_SELECTOR, "#product-link356110 > div:nth-child(3) > div:nth-child(2) > div:nth-child(2) > div:nth-child(3) > button:nth-child(2)")
# time.sleep(3)
# savatcha1.click()
# driver.execute_script("arguments[0].click();", savatcha1)
# time.sleep(13)

# scroll the website or webpage to the complete body height
driver.close()
