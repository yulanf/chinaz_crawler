import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities.CHROME
caps['loggingPrefs'] = {'performance': 'ALL'}
driver = webdriver.Chrome(desired_capabilities=caps)

driver.get('https://www.baidu.com')


# # print(type(driver.get_log('performance')))

# with open('devtools', 'w') as f:
#     for log in driver.get_log('performance'):
#         f.write(log + '\n')


logs = [json.loads(log['message'])['message'] for log in driver.get_log('performance')]

with open('devtools.json', 'w') as f:
    json.dump(logs, f)

driver.close()