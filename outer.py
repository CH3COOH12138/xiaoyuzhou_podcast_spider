from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# 设置 Chrome 无头模式（可选）
options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.page_load_strategy = 'normal'
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
# options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://xyzrank.com/#/hot-podcasts")

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div[3]/div[2]/div/div[2]/table/tbody/tr[29]")))

    # print(driver.page_source)
    # 获取所有目标链接
    links = driver.find_elements(
        By.XPATH, "/html/body/div/div[3]/div[2]/div/div[2]/table/tbody/tr/td[12]/span/a[1]")

    # 提取 href 属性
    href_list = [link.get_attribute("href") for link in links if link.get_attribute("href")]

    # 保存到 CSV 文件
    with open("podcast_links.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Index", "Link"])  # 写入标题
        for index, href in enumerate(href_list, 1):
            writer.writerow([index, href])

    print(f"成功保存 {len(href_list)} 条链接到 podcast_links.csv")

finally:
    driver.quit()