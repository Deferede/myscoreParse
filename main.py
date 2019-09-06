import urllib.request
import csv
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

SITE_URL = 'https://joblab.ru'
def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def save(links_to_job, path):
    with open(path, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow((
            'Объявление',
            'Ссылка на объявление',
            'Организация',
            'Ссылка на организацию',
            'Город',
            'Телефон',
            'Email',
            'Контактное лицо',
            'Характер работы',
            'Заработная плата',
            'Условия',
            'График работы',
            'Обязанности',
            'Образование',
            'Опыт работы',
            'Требования'
            ))

        for job in links_to_job:
            writer.writerow((
                job['job_title'],
                job['job_href'],
                job['org'],
                job['org_link'],
                job['city'],
                job['phone'],
                job['email'],
                job['contact'],
                job['job_character'],
                job['price'],
                job['conditions'],
                job['graph'],
                job['duties'],
                job['education'],
                job['job_exp'],
                job['requires']
                ))


def clearString(string):
    new_string = string.replace(" ", "").replace("(","").replace(")", "")
    return new_string

def parse(html, filename):
    result_arr = []

    soup = BeautifulSoup(html, 'lxml')

    tr = soup.find('div', {"id" : 'direct_1'}).findNext('table').find_all('tr')
    a = soup.find('td', class_='contentmain').find_all('table')[5].find_all('p', class_='prof')
    links_to_job = []

    for job in tr:

        try:
            job_title = job.find('p', class_='prof').find('a').text.strip()
            job_href = job.find('p', class_='prof').find('a').get('href')
            try:
                city = job.find('td', class_='td-to-div-city').find_all('p')[1].text
            except Exception as e:
                city = job.find('td', class_='td-to-div-city').find_all('p')[0].text
            org = job.find('p', class_='org').find('a').text
            org_link = job.find('p', class_='org').find('a').get('href')
        except Exception as e:
            continue
        

        links_to_job.append({
            'job_title': job_title,
            'job_href': SITE_URL + job_href,
            'org': org,
            'org_link': SITE_URL + org_link,
            'city': city,
            })
        
        
    browser = webdriver.Firefox()
    i = 0
    for link in links_to_job:
        print ('Парсинг %d%%' % (i / len(links_to_job) * 100))

        
        browser.get(link['job_href'])
        browser.execute_script("cp()")
        browser.execute_script("cm()")
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        try:
            phone = browser.find_element_by_id("p").text
        except Exception as e:
            phone = ''
        try:
            email = browser.find_element_by_id("m").text
        except Exception as e:
            email = ''
        try:
            contact = soup.find('p', text = "Контактное лицо").parent.findNext('td').text.split(';')[1]
        except Exception as e:
            contact = ''
        try:
            job_character = soup.find('p', text = "Характер работы").parent.findNext('td').text.replace(";", "")
        except Exception as e:
            job_character = ''
        try:
            price = soup.find('p', text = "Заработная плата").parent.findNext('td').text.replace(";", "")
        except Exception as e:
            price = ''
        try:
            conditions = soup.find('p', text = "Условия").parent.findNext('td').text.replace(";", "")
        except Exception as e:
            conditions = ''
        try:
            graph = soup.find('p', text = "График работы").parent.findNext('td').text.replace(";", "")
        except Exception as e:
            graph = ''
        try:
            duties = soup.find('p', text = "Обязанности").parent.findNext('td').text.replace(";", "")
        except Exception as e:
            duties = ''
        try:
            education = soup.find('p', text = "Образование").parent.findNext('td').text.replace(";", "")
        except Exception as e:
            education = ''
        try:
            job_exp = soup.find('p', text = "Опыт работы").parent.findNext('td').text.replace(";", "")
        except Exception as e:
            job_exp = ''
        try:
            requires = soup.find('p', text = "Требования").parent.findNext('td').text.replace(";", "")
        except Exception as e:
            requires = ''
        link['contact'] = contact
        link['phone'] = phone
        link['email'] = email
        link['job_character'] = job_character
        link['price'] = price
        link['conditions'] = conditions
        link['graph'] = graph
        link['duties'] = duties
        link['education'] = education
        link['job_exp'] = job_exp
        link['requires'] = requires

        i += 1

    browser.quit()

    save(links_to_job, filename + '.csv')

def main():
    f = open('url.txt', 'r')
    i = 0
    for x in f:
        html = get_html(x)
        parse(html,'file'+ str(i))
        i += 1


if __name__ == '__main__':
    main()