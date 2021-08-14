import math
import sys
import threading
import time
import logging
from selenium import webdriver

CHROME_EXECUTED_PATH = "./chromedriver.exe"
POPCAT_url = 'https://popcat.click/'


log = logging.getLogger()
format = '%(asctime)s: %(message)s'

stream = logging.StreamHandler(stream=sys.stdout)
stream.setLevel(logging.INFO)
stream.setFormatter(logging.Formatter(format))
log.addHandler(stream)

class CountDownTimer:
    isSleep = False
    initial_time = time.time()

    @staticmethod
    def sleeptimer(sec):
        CountDownTimer.isSleep = True
        time.sleep(sec)
        CountDownTimer.isSleep = False
        pass

    @staticmethod
    def timer():
        while CountDownTimer.isSleep:
            time.sleep(1)
            current = math.floor(time.time() - CountDownTimer.initial_time)
            log.info(f'Executed: {current}')


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--test-type')
driver = webdriver.Chrome(executable_path=CHROME_EXECUTED_PATH, chrome_options=options)
driver.get(POPCAT_url)
time.sleep(1)

try:
    xpath_click = '//*[@id="app"]/div'
    click_ = driver.find_element_by_xpath(xpath=xpath_click)
except Exception as e:
    log.error(e)
    exit(1)

sleep_timer = threading.Thread(target=CountDownTimer.sleeptimer, args=(60000,), daemon=True)
timer = threading.Thread(target=CountDownTimer.timer(), daemon=True)
sleep_timer.start()
timer.start()

while CountDownTimer.isSleep:
    click_.click()
    time.sleep(0)

while log.handlers:
    handler = log.handlers[0]
    handler.close()
    log.removeHandler(handler)