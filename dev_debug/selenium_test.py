# 一个简单的检查 selenium 环境是否搭建好的内容

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By  
from selenium.webdriver.chrome.service import Service  
  
browser = webdriver.Chrome()  
  
browser.get('http://www.baidu.com')  
search = browser.find_element(By.ID, 'kw')  
search.send_keys('python')  
search.send_keys(Keys.ENTER)  
  
# browser.close()