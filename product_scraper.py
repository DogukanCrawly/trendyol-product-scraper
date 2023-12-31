import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from database_manager import DatabaseManager

class ProductScraper:
    def __init__(self, url, product_count=15, name='product'):
        self.url = url
        self.name = name
        self.product_count = product_count
        self.counter = 1
        self.all_products = pd.DataFrame(columns=['ID', 'brandName', 'productName', 'commentCount', 'price'])
        self.database_manager = DatabaseManager()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    # Verileri çekerken gelen gereksiz boşluk, noktalama işaretlerini kaldıran fonksiyon
    def _string_editor(self, text):
        return text.replace('(', '').replace(')', '').replace('TL', '').replace(' ', '')

    # Ürünün iç bilgilerini çekiyor
    def _scrape_product_info(self, product_element):
        try:
            comment = int(self._string_editor(product_element.find_element(By.CLASS_NAME, 'ratingCount').text))
        except:
            comment = 0
        product_ID = int(self.counter)
        product_name = product_element.find_element(By.CLASS_NAME, 'prdct-desc-cntnr-name').text
        product_brand = product_element.find_element(By.CLASS_NAME, 'prdct-desc-cntnr-ttl').text
        price = int(round(float(self._string_editor(product_element.find_element(By.CLASS_NAME, 'prc-box-dscntd').text.replace('.', '').replace(',', '.')))))
        return {'ID': product_ID, 'brandName': product_brand, 'productName': product_name, 'commentCount': comment, 'price': price}

    # Url ve kaç tane çekmek istediğine göre linkteki ürünleri alıyor
    def scrape_products(self):
        for i in self._to_infinity():
            if self.counter <= self.product_count:
                current_url = f'{self.url}&pi={i}'
                self.driver.get(current_url)
                products = self.driver.find_elements(By.CLASS_NAME, 'p-card-wrppr ')

                # Sorted özelliği ile büyükten küçüğe sıralıyoruz

                for product in sorted(products, key=lambda p: self._get_price(p)):
                    if self.counter <= self.product_count:
                        product_info = self._scrape_product_info(product)
                        self.all_products = pd.concat([self.all_products, pd.DataFrame([product_info])],
                                                      ignore_index=True)
                        self.counter += 1
                    else:
                        break
            else:
                break

    # Fiyatları almak için yardımcı fonksiyon
    def _get_price(self, product):
        try:
            price_text = product.find_element(By.CLASS_NAME, 'prc-box-dscntd').text
            return float(price_text.replace('.', '').replace(',', '.'))
        except:
            return float('inf')

    def _to_infinity(self):
        index = 0
        while True:
            yield index
            index += 1

    # Konsola ürünleri yazmamızı sağlayan fonksiyon
    def print_products(self):
        print(self.all_products)
        print(len(self.all_products))

    # Ürünleri excel şablonuna basmamızı sağlayan fonksiyonu çağırıyor
    def to_excel(self, excel_file='products_data'):
        # Write the data to an Excel file
        self.all_products.sort_values(by=['price'], inplace=True)
        self.all_products.to_excel(excel_file + '.xlsx', index=False)

    # Ürünleri veri tabanına yazan fonksiyonu çağırıyor
    def write_to_database(self):
        self.database_manager.create_table()
        sorted_products = self.all_products.sort_values(by=['price'])
        self.database_manager.write_to_database(sorted_products)

    # chromedriverı kapatıyor.
    def close_driver(self):
        self.driver.close()