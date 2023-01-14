from selenium import webdriver
from selenium.webdriver.common.keys import Keys

mobile = "手机号或者用户名"

password = "密码"

browser = webdriver.Firefox()
browser.get("https://www.huixx.cn/")
browser.find_element_by_id("login_btn").click()

browser.find_element_by_class_name("go_account").click()
browser.find_element_by_name("mobile").send_keys(mobile)
browser.find_element_by_name("password").send_keys(password)

oldCookies = browser.get_cookies()

browser.find_element_by_class_name("btn-account-login").click()

cookies = browser.get_cookies()

if cookies == oldCookies :
    print("[Error] login fail")
else :
    f = open("./tmp/_huixx.cn_cookie.tmp","w")
    f.write(cookies)

    f.close()

browser.quit()