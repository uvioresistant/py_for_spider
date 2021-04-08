from selenium import webdriver
browser = webdriver.PhantomJS()
browser.get('https://baidu.com')
print(browser.current_url)