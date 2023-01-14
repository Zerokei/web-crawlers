# 简单版本的，没有进行验证的爬取猫眼电影
import requests
import time
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76',
}

pages = []  # 存储每一页的 HTML
top_movies = []  # 从 HTML 中提取数据

def set_pages():
    for i in range(10):
        response = requests.get('https://www.maoyan.com/board/4?offset={}'.format(i * 10), headers=headers)
        pages.append(response.text)
        print("已获取第{}页".format(i + 1))
        # 间隔 1 秒时间，防止过于频繁
        time.sleep(1)

def extract_data():
    for i in range(10):
        extract_element(pages[i])

def extract_element(text):
    # print(text)
    html = etree.HTML(text)
    # 提取各种元素
    numbers = html.xpath('//div[@class="content"]/div/div/dl/dd/i/text()')
    movies = html.xpath('//div[@class="content"]/div/div/dl/dd/div/div/div/p/a/text()')
    stars = html.xpath('//div[@class="content"]/div/div/dl/dd/div/div/div/p[@class="star"]/text()')
    releasetimes = html.xpath(
        '//div[@class="content"]/div/div/dl/dd/div/div/div/p[@class="releasetime"]/text()')
    scores_interger = html.xpath(
        '//div[@class="content"]/div/div/dl/dd/div/div/div/p[@class="score"]/i[@class="integer"]/text()')
    scores_fraction = html.xpath(
        '//div[@class="content"]/div/div/dl/dd/div/div/div/p[@class="score"]/i[@class="fraction"]/text()')
    for i in range(10):
        movie = []
        movie.append(numbers[i])
        movie.append(movies[i])
        movie.append(stars[i].replace('\n', '').strip())
        movie.append(releasetimes[i])
        movie.append(scores_interger[i] + scores_fraction[i])
        # 加入top movies列表中
        top_movies.append(movie)

def save_data():
    open('top_100.txt', 'w').close()
    for i in range(100):
        with open('top_100.txt', 'a', encoding='utf-8')as f:
            print(top_movies[i], file=f)

def main():
    set_pages()
    extract_data()
    save_data()

if __name__ == '__main__':
    main()
