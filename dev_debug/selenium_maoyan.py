# 如果输出的是 UTF-8 utf-8，那么就代表正确进入到了 iframe  
# 不过这个必须要保证访问 TOP 100 时出现的是验证中心
from selenium import webdriver  
from selenium.webdriver.common.by import By  
import time  
  
broswer = webdriver.Chrome()  
broswer.get('https://tfz.maoyan.com/yamaha/verify#/')  
time.sleep(5)  
iframe = broswer.find_elements(By.TAG_NAME, "iframe")[0]  
  
broswer.switch_to.frame(iframe)  
element = broswer.find_element(By.XPATH, '//head/meta')  
print(element.get_attribute('charset')) # UTF-8  
  
broswer.switch_to.default_content()  
elements = broswer.find_element(By.XPATH, '//head/meta')  
print(elements.get_attribute('charset')) # utf-8