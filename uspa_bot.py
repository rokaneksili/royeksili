from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Tarayıcıyı başlat
driver = webdriver.Chrome()  # veya webdriver.Firefox() vb.

# Giriş yapılacak site URL'si
login_url = "https://www.uspalastik.com/index.php?url=account/logout"

# Kullanıcı adı ve şifre
username = "ekremeksili@gmail.com"
password = "123456"

# Tarayıcıyı giriş yapılacak URL'ye yönlendir
driver.get(login_url)

# Kullanıcı adı ve şifreyi giriş formuna yaz
username_input = driver.find_element(By.NAME, "email")
password_input = driver.find_element(By.NAME, "password")
username_input.send_keys(username)
password_input.send_keys(password)

# Giriş yap butonuna tıkla
login_button = driver.find_element(By.XPATH, "//div[@class='ui fluid huge orange submit button']")
login_button.click()

# Sayfanın yüklenmesini bekle
WebDriverWait(driver, 10).until(EC.url_to_be("https://www.uspalastik.com/index.php?url=bayi/siparis/lastik&path=36"))

# Verileri saklamak için bir liste oluştur
all_data = []

# Son sayfa numarasını belirtin
last_page_number = int(input("Lütfen veri çekmek istediğiniz son sayfa numarasını girin: "))  # Örneğin, son sayfa numarası 5 ise bunu değiştirin

for page in range(1, last_page_number + 1):
    # Sayfa numarasına göre URL'yi oluştur
    data_url = f"https://www.uspalastik.com/index.php?url=bayi/siparis/lastik&path=36&page={page}"
    
    # Veri almak için tarayıcıyı yönlendir
    driver.get(data_url)
    
    # Sayfanın yüklenmesini bekle
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
    
    # Sayfanın HTML içeriğini al
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Verileri çek
    rows = soup.find_all("tr", class_="heading")
    for row in rows[1:]:
        cols = row.find_all("td")
        data = [col.text.strip() for col in cols]
        all_data.append(data)

# Listeyi bir Pandas DataFrame'e dönüştür
df = pd.DataFrame(all_data)

# İstenmeyen sütunları çıkar
columns_to_drop = [0, 2, 4, 10, 11, 12]
df.drop(columns_to_drop, axis=1, inplace=True)

# Sütun adlarını belirle
column_names = {
    3: 'Ürün Kodu',
    5: 'Ürün Açıklama',
    6: 'Dot',
    7: 'Etiket',
    8: 'Fiyat',
    9: 'Stok'
}

# Sütun adlarını atama
df.rename(columns=column_names, inplace=True)

# Excel dosyasına yaz
df.to_excel("uspa_bot.xlsx", index=False)

print("Veriler başarıyla uspa_bot.xlsx dosyasına kaydedildi.")

# Tarayıcıyı kapat
driver.quit()
