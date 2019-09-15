from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

SITE_URL = 'https://www.myscore.ru/'


def init_browser(headless=False, browser='firefox'):
    options = Options()

    options.headless = headless
    if browser == 'firefox':
        profile = webdriver.FirefoxProfile()
        # 1 - Allow all images
        # 2 - Block all images
        # 3 - Block 3rd party images
        profile.set_preference("permissions.default.image", 2)
        browser = webdriver.Firefox(executable_path='geckodriver.exe', firefox_profile=profile, options=options)
        # browser = webdriver.Firefox(firefox_profile=profile, options=options)
        print ("Firefox Initialized")
    elif browser == 'chrome':
        browser = webdriver.Firefox(options=options)
        print ("Chrome Initialized")
    browser.implicitly_wait(30)
    browser.set_window_position(0, 0)
    # browser.set_window_size(360, 240)
    return browser

def get_browser_BS_html(browser):
    loadingOverlay = browser.find_element_by_class_name('loadingOverlay')
    WebDriverWait(browser, 30, ignored_exceptions=True).until(EC.invisibility_of_element(loadingOverlay))
    html = BeautifulSoup(browser.page_source, 'lxml')
    return html

def get_matchs_id():
    browser = init_browser()
    browser.implicitly_wait(30)
    browser.get(SITE_URL)
    matchs_id = []
    loadingOverlay = browser.find_element_by_class_name('loadingOverlay')
    WebDriverWait(browser, 30, ignored_exceptions=True).until(EC.invisibility_of_element(loadingOverlay))
    browser.find_element_by_class_name('calendar__direction--yesterday').click()
    html = get_browser_BS_html(browser)
    divs = html.find_all('div', class_='event__match')
    for div in divs:
        id = div.get('id')
        if id.startswith('g_1'):
            matchs_id.append({
            'id': id[4:]
            })

    for i in range(8):
        print ('Листинг {}%'.format(float((i / 8 * 100))))
        try:
            WebDriverWait(browser, 30, ignored_exceptions=True).until(EC.invisibility_of_element(loadingOverlay))
            browser.find_element_by_class_name('calendar__direction--tomorrow').click()
            WebDriverWait(browser, 30, ignored_exceptions=True).until(EC.invisibility_of_element(loadingOverlay))
            html = BeautifulSoup(browser.page_source, 'lxml')
            divs = html.find_all('div', class_='event__match')
            for div in divs:
                id = div.get('id')
                if id.startswith('g_1'):
                    matchs_id.append({
                        'id': id[4:]
                    })
        except Exception as e:
            print('Завтра больше нет=(')
    browser.quit()
    return matchs_id