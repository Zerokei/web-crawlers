# 这个是单独访问他的验证中心，探究 selenium 是否正常运行了

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
import cv2
from selenium.webdriver import ActionChains
import requests
from io import BytesIO

class MaoYanCode(object):
    def __init__(self,inputUrl):    # 初始化
        self.url = inputUrl
        ChromeOptions = webdriver.ChromeOptions()
        ChromeOptions.add_argument('--ignore-certificate-errors') # 减少一些奇怪的报错
        ChromeOptions.add_argument('--ignore-ssl-errors')
        self.browser = webdriver.Chrome(options=ChromeOptions)
        self.wait = WebDriverWait(self.browser, 30)

    def open(self):        # 打开网页
        self.browser.get(self.url)

    def bg_img_src(self):    # 定位背景图
        bg_img_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="tc-bg"]/img')))
        bg_img_src = bg_img_element.get_attribute('src')
        return bg_img_src

    def tp_img_src(self):    # 定位缺块
        target_img_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="tc-jpp"]/img')))
        target_img_src = target_img_element.get_attribute('src')
        return target_img_src

    def get_img(self):    # 获取背景和缺块图片
        bg_src = self.bg_img_src()
        tp_src = self.tp_img_src()
        response1 = requests.get(bg_src)
        image1 = Image.open(BytesIO(response1.content))
        image1.save('bg_img.png')

        response2 = requests.get(tp_src)
        image2 = Image.open(BytesIO(response2.content))
        image2.save('tp_img.png')
        return image1, image2

    def slider_element(self):    # 定位滑块
        time.sleep(2)
        slider = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@class="tc-drag-thumb"]')))
        return slider

    def get_gap(self, gap_img):
        bg_img = cv2.imread('bg_img.png')
        tp_img = cv2.imread('tp_img.png')

        bg_edge = cv2.Canny(bg_img, 100, 200)  # 识别图片边缘
        tp_edge = cv2.Canny(tp_img, 100, 200)

        # cv2.imwrite('bg_edge.png', bg_edge)
        # cv2.imwrite('tp_edge.png', tp_edge)  # 保存图片边缘文件到本地

        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)  # 转换图片格式
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)  # 灰度图片转为RGB彩色图片

        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)  # 缺口匹配
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

        # # 绘制方框，验证匹配效果
        # height, width = tp_pic.shape[:2]  # img.shape[:2] 获取图片的长、宽
        # tl = max_loc  # 左上角点的坐标
        # cv2.rectangle(bg_img, tl, (tl[0] + width - 15, tl[1] + height - 15),(0, 0, 255), 2)  # 绘制矩形
        # cv2.imwrite(gap_img, bg_img)  # 保存图片缺口识别结果在本地

        return max_loc[0]  # 返回缺口的X坐标

    # 构造移动轨迹
    def get_track(self, distance):  # 获得移动轨迹
        track = []  # 移动轨迹
        current = 0  # 当前位移
        mid = distance * 4 / 5
        t = 0.2
        v = 0
        while current < distance:
            if current < mid:
                a = 5
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track

    # 移动滑块
    def move_to_gap(self, slider, track):
        ActionChains(self.browser).click_and_hold(slider).perform()  # click_and_hold()按住底部滑块
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x,yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def login(self):
        self.open()
        time.sleep(10)  # 网速原因可能导致网页加载不完全，致使iframe报错
        # 获得 title
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//title')))
        title = self.browser.title
        if title != '猫眼验证中心':
            time.sleep(10)
            html = self.browser.page_source
            print('selenium title is not check center: ', title)
            return html
        iframe = self.wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'iframe')))
        self.wait.until(EC.frame_to_be_available_and_switch_to_it(iframe[0]))
        self.get_img()
        slider = self.slider_element()
        slider.click()
        gap = self.get_gap('result.png')
        gap_end = int((gap - 40) / 2)  # 页面和图片的大小不同，需要更改比例
        gap_end -= 10  # 减去缺块白边
        track = self.get_track(gap_end)  # 获取移动轨迹
        self.move_to_gap(slider, track)  # 拖动滑块
        # 等待所有都加载完，获得当前页面 html
        time.sleep(10)
        html = self.browser.page_source
        return html

def main():
    spider = MaoYanCode('https://tfz.maoyan.com/yamaha/verify#/')
    html = spider.login()
    # print(html)

if __name__ == '__main__':
    main()