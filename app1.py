import os
import os as sistema
from random import randint
from subprocess import CREATE_NO_WINDOW
from time import sleep

import scrapy
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc


#  '--incognito', 
def iniciar_driver():
    ua  =  UserAgent( browsers = ['chrome'])
    arguments = [f'user-agent={ua.random}',]
    chrome_options = Options()

    arguments = [f'user-agent={ua.random}','--lang=pt-BR', '--window-size=1300,5000','--incognito','disable-infobars','--disable-extensions','--disable-blink-features=AutomationControlled']

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
    chrome_options.add_experimental_option("useAutomationExtension", False) 
    chrome_options.add_experimental_option('prefs', {
        # Notificar o google chrome sobre essa alteração
        'download.directory_upgrade': True,
        # Desabilitar confirmação de download
        'download.prompt_for_download': False,
        # Desabilitar notificações
        'profile.default_content_setting_values.notifications': 2,
        # Permitir multiplos download
        'profile.default_content_setting_values.automatic_downloads': 1,
        # Remover cookie
        # 'profile.default_content_setting_values.cookies': 2,
        # Remover todos os erros e avisos
        "excludeSwitches": ['disable-logging']
    })

    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_service.creation_flags = CREATE_NO_WINDOW
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver


def digitar_naturalmente(texto, elemento):
    for letra in texto:
        elemento.send_keys(letra)
        sleep(randint(1, 5)/20)


class ShopeeSpider(scrapy.Spider):
    name = "shopee"

    def ex_shopee(self, item_teste):
        self.item_teste1 = item_teste
        usuario = sistema.getlogin()

        os.chdir(os.path.join(os.path.expanduser('~'),'desktop'))

        if(os.path.exists('shopee.csv')):
                
            x = 0
            while True:
                if(os.path.exists(f'shopee{x}.csv')):
                    x += 1
                else:
                    arquivo1 = (f'shopee{x}.csv')
                    break

            ba = (f'C:/Users/{usuario}/Desktop/{arquivo1}')
            process = CrawlerProcess(settings = {'FEEDS': {arquivo1:{'format':'csv',}}})
            with open(arquivo1,"w") as arq1:
                arq1.write(self.item_teste1)
                arq1.close
            process.crawl(ShopeeSpider)
            process.start()

        else:
            ba = (f'C:/Users/{usuario}/Desktop/shopee.csv')
            process = CrawlerProcess(settings = {'FEEDS': {'shopee.csv':{'format':'csv',}}})
            with open('shopee.csv',"w") as arq1:
                arq1.write(self.item_teste1)
                arq1.close
            process.crawl(ShopeeSpider)
            process.start()

    def start_requests(self):
        usuario = sistema.getlogin()

        os.chdir(os.path.join(os.path.expanduser('~'),'desktop'))

        if(os.path.exists('shopee.csv')):
                
            x = 0
            while True:
                if(os.path.exists(f'shopee{x}.csv')):
                    x += 1
                else:
                    if x == 0:
                        arquivo2 = ('shopee.csv')
                        break
                    else:
                        y = x - 1
                        arquivo2 = (f'shopee{y}.csv')
                        break
            ba = (f'C:/Users/{usuario}/Desktop/{arquivo2}')
        else:
            ba = (f'C:/Users/{usuario}/Desktop/shopee.csv')
        
        with open (arquivo2, 'r', encoding='utf-8') as arquivo:
            teste= arquivo.read()
        busque_item = teste
        options = uc.ChromeOptions()
        arguments = ['--window-size=1300,5000',]
        for argument in arguments:
            options.add_argument(argument)
        self.driver = uc.Chrome() 
        # self.driver = iniciar_driver()
        self.driver.get("https://www.shopee.com.br/")
        sleep(10)
        self.driver.refresh()
        sleep(5)

        campo_buscar = self.driver.find_element(By.XPATH, "//input[@class='shopee-searchbar-input__input']")
        campo_buscar.click()
        sleep(1)
        digitar_naturalmente(busque_item, campo_buscar)
        sleep(2)
        btn_procurar = self.driver.find_element(By.XPATH, "//button[@class='btn btn-solid-primary btn--s btn--inline shopee-searchbar__search-button']")
        sleep(3)
        btn_procurar.click()
        sleep(0.1)
        url_item = self.driver.current_url
        sleep(2.1)
        self.driver.get(url_item)
        sleep(3)
        self.driver.execute_script('window.scrollTo(0, 1000);')
        sleep(5)
        self.driver.execute_script('window.scrollTo(0, 2000);')
        sleep(5)
        self.driver.execute_script('window.scrollTo(0, 3000);')
        sleep(5)
        self.driver.execute_script('window.scrollTo(0, 4000);')
        sleep(5)
        url_inicial = self.driver.current_url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        yield scrapy.Request(url=url_inicial, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for i in soup.find_all("div",class_='col-xs-2-4 shopee-search-item-result__item'):
            titulo = i.find("div", class_='ie3A+n bM+7UW Cve6sh').get_text()
            preco2 = i.find("span", class_='ZEgDH9').get_text()
            preco1 = str(preco2).replace('.', '')
            preco = str(preco1).replace(',', '.')
            estado = i.find("div", class_='zGGwiV').get_text()
            link1 = i.find("a").get('href')
            link = f'https://www.shopee.com.br{link1}'
            
            yield {
                ' - Titulo': titulo,
                'Preco': preco,
                'Estado': estado,
                'link': link
            }

        next_page = soup.find("span", class_='shopee-mini-page-controller__total').get_text()
        num_total = int(next_page)
        num = 1
        if num != num_total:
            btn_proximo = self.driver.find_element(By.XPATH, "//button[@class='shopee-icon-button shopee-icon-button--right ']")
            sleep(3)
            btn_proximo.click()
            sleep(5)
            sleep(3)
            self.driver.execute_script('window.scrollTo(0, 1000);')
            sleep(5)
            self.driver.execute_script('window.scrollTo(0, 2000);')
            sleep(5)
            self.driver.execute_script('window.scrollTo(0, 3000);')
            sleep(5)
            self.driver.execute_script('window.scrollTo(0, 4000);')
            sleep(5)
            num += 1
            url_proximo = self.driver.current_url
            yield scrapy.Request(url=url_proximo, headers=self.headers, callback=self.parse)
        else:
            self.driver.close
        self.driver.close


