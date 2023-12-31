from product_scraper import ProductScraper
from unidecode import unidecode

def convert_to_url_format(product_name):
    # Türkçe karakterleri ASCII ye göre düzenliyor
    product_name = unidecode(product_name)
    # Küçük harfe çevir, boşlukları '-' ile değiştir ve URL formatına uygun hale getir
    return product_name.lower().replace(' ', '-')

if __name__ == "__main__":
    # Kullanıcıdan ürün adını al
    name = input("Ürün adını girin: ")
    product_count = int(input("Çekilecek ürün adedi: "))
    product_name = convert_to_url_format(name)


    # URL'yi oluştur
    url = f'https://www.trendyol.com/sr?q={product_name}&t={product_name}&st={product_name}'

    # ProductScraper oluştur
    product_scraper = ProductScraper(name=name, url=url, product_count=product_count)

    # Ürünleri çek, veritabanına yaz ve Excel'e kaydet
    product_scraper.scrape_products()
    product_scraper.write_to_database()
    product_scraper.to_excel()
    product_scraper.close_driver()

    # Veritabanından ürünleri fiyatı 100'den küçük olanları seç ve ekrana yazdır
    product_db = product_scraper.database_manager
    product_result = product_db.get_from_db_by_query(f"SELECT productName, commentCount, price FROM product_data WHERE price < 100")
    print(product_result)
