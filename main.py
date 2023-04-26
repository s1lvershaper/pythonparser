import aiohttp
import asyncio
import logging
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    filename='error.log',
    filemode='a',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.3"}

async def fetch_html(url, session):
    try:
        async with session.get(url, headers=Headers, timeout=10) as response:
            return await response.text()
    except aiohttp.ClientError as e:
        logging.error(f"Error fetching {url}: {e}")

async def get_coin_price():
    url = "https://lenta.ru/"
    with open('result.txt', 'w', encoding='utf-8') as f:
        async with aiohttp.ClientSession() as session:
            while True:
                response = await fetch_html(url, session)
                if response:
                    bs = BeautifulSoup(response, 'html.parser')
                    temp_list = bs.find_all('span', class_="card-mini__title")
                    for temp in set(temp_list):
                        text = temp.text.strip()
                        if text and (text.isascii() or any(ord(c) > 127 for c in text)):
                            f.write(text + '\n')
                            print(text)
                await asyncio.sleep(10)

executor = ThreadPoolExecutor(max_workers=8)
loop = asyncio.get_event_loop()
loop.run_until_complete(get_coin_price())