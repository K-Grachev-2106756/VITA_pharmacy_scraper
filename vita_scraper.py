from selenium import webdriver
import bs4
import json 
from selenium.webdriver.common.by import By
import time




#page for getting categories
driver = webdriver.Chrome()
driver.get('https://vitaexpress.ru/catalog/lekarstva-i-bady/')
html = driver.page_source

with open('vita.html', 'w', encoding='utf-8') as f:
    f.write(html)


#categories
soup = bs4.BeautifulSoup(html, 'lxml')
categories = soup.find('div', class_ = 'subCat__list').find_all(class_ = 'subCat__link left-content')
cat_list = []
for cat in categories:
    cat_list.append(cat.get('href'))

with open('categories.json', 'w', encoding='utf-8') as f:
    json.dump(cat_list, f, ensure_ascii=False, indent=4)


#FULL pages for getting inf about ALL goods (this part worked for about 75 min)
categories = []
with open('categories.json', 'r') as f:
    categories = json.loads(f.read())

for cat in categories:
    link = 'https://vitaexpress.ru' + cat
    driver = webdriver.Chrome()
    driver.get(link)
    time.sleep(5)
    confirm_btn =  driver.find_element(By.XPATH, '//a[@class="pointer help-city__btn btn btn-large btn-primary"]')
    confirm_btn.click()
    while(True):
        try:
            for i in range(5):
                driver.execute_script(f'window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(1)
            driver.find_element(By.ID, 'newBtnPager').click()   
            time.sleep(3)    
        except:
            for i in range(50):
                driver.execute_script(f'window.scrollTo({i}, {i+1}*document.body.scrollHeight/50);')
                time.sleep(1)
            break
       
    html = driver.page_source

    name = cat.split(r'/')[3]
    with open(name + '.html', 'w', encoding = 'utf-8') as ff:
        ff.write(html)


#ALL goods
for cat in categories:
    name = cat.split(r'/')[3]
    with open(name + '.html', 'r', encoding = 'utf-8') as f:
        soup = bs4.BeautifulSoup(f.read(), 'lxml')
        goods = soup.find_all('div', class_="product-hor mb-10 js-stateProduct")
        
        info = []
        for product in goods:
            product_name_ = product.get('data-name')
            product_url_ = product.get('dathora-url')
            product_brand_ = product.get('data-brand')
            product_category_1_ = product.get('data-item-category1')
            product_category_2_ = product.get('data-item-category2')
            product_price_ = product.get('data-price')
            active_substance_ = product.find(class_ = 'search-mnn-highlight d-inline-block mt-8')
            if (active_substance_ != None) :
                active_substance_ = active_substance_.text[24:-5]
            
            info.append({
                'product_name': product_name_,
                'product_url': product_url_,
                'product_brand': product_brand_,
                'product_category_1': product_category_1_,
                'product_category_2': product_category_2_,
                'product_price': product_price_,
                'active_substance': active_substance_
            })
        
        with open(name+'.json', 'w', encoding='utf-8') as ff:
            json.dump(info, ff, ensure_ascii=False, indent=4)
