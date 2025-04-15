import pandas as pd
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# 初始化 WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 无头模式
options.add_argument('--disable-gpu')
service = Service(executable_path='chromedriver')  # 请确保 chromedriver 在 PATH 中或指定完整路径
driver = webdriver.Chrome(service=service, options=options)

# 读取 podcast_links.csv 的第二列（从第 0 行开始，索引为 1）
df = pd.read_csv('podcast_links.csv', header=None)
urls = df[1].tolist()  # 获取第二列

# 打开目标 CSV 文件准备写入
with open('extracted_links.csv', 'w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)

    # 遍历每个 URL
    for url in urls:
        print(url)
        try:
            driver.get(url)
            time.sleep(0.5)  # 等待页面加载，可根据需要调整

            # 抓取所有符合 XPath 的 <a> 元素
            elements = driver.find_elements(By.XPATH, '/html/body/div/div[1]/main/main/div[2]/ul/li[*]/a')
            hrefs = [el.get_attribute('href') for el in elements if el.get_attribute('href')]

            # 将该页的所有 href 写成一行
            writer.writerow(hrefs)

        except Exception as e:
            print(f"抓取 {url} 时出错: {e}")
            writer.writerow([])  # 出错时写入空行，保持对应行数一致

# 关闭 WebDriver
driver.quit()
