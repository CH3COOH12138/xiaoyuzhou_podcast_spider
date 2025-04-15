import pandas as pd
import subprocess
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 配置 Selenium
chrome_options = Options()
chrome_options.add_argument('--headless')  # 无头模式
chrome_options.add_argument('--disable-gpu')
service = Service('chromedriver')  # 替换为你的 chromedriver 路径
driver = webdriver.Chrome(service=service, options=chrome_options)

# 输出文件夹
output_dir = 'F:/music/origin'
os.makedirs(output_dir, exist_ok=True)

# 读取 extracted_links.csv 的第一列
df = pd.read_csv('extracted_links.csv', header=None)
urls = df[0].dropna().tolist()

# 定义 .m4a 链接正则
m4a_pattern = re.compile(r'https?://[^\s"\']+?\.m4a')

# 遍历所有链接
for idx, url in enumerate(urls, start=300):
    try:
        print(f'[{idx}] 正在访问: {url}')
        driver.get(url)
        time.sleep(2)  # 等待页面加载

        # 获取页面源码
        page_source = driver.page_source

        # 提取 .m4a 链接
        m4a_links = m4a_pattern.findall(page_source)
        if not m4a_links:
            print(f'[{idx}] 未找到 .m4a 链接')
            continue

        m4a_url = m4a_links[0]  # 取第一个 .m4a 链接
        print(f'[{idx}] 找到 .m4a: {m4a_url}')

        # 构建输出文件路径
        output_path = os.path.join(output_dir, f"{idx}.mp3")

        # 构造 ffmpeg 命令
        cmd = [
            "ffmpeg",
            "-ss", "360",  # 从 60 秒开始
            "-i", m4a_url,  # 输入文件
            "-t", "180",  # 截取 1800 秒
            "-acodec", "libmp3lame",  # 编码为 MP3
            "-b:a", "128k",  # 比特率 128k
            output_path
        ]

        # 执行命令
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f'[{idx}] 下载完成：{output_path}')

    except Exception as e:
        print(f'[{idx}] 出错: {e}')

# 关闭浏览器
driver.quit()
