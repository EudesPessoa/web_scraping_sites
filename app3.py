import scrapy
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from time import sleep
from random import randint
from bs4 import BeautifulSoup
import re
from scrapy.crawler import CrawlerProcess
import os as sistema
import os
from subprocess import CREATE_NO_WINDOW

# '--headless',
def iniciar_driver():
    chrome_options = Options()

    arguments = ['--lang=pt-BR', '--window-size=1300,1000', '--incognito', ]

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        # Notificar o google chrome sobre essa alteração
        'download.directory_upgrade': True,
        # Desabilitar confirmação de download
        'download.prompt_for_download': False,
        # Desabilitar notificações
        'profile.default_content_setting_values.notifications': 2,
        # Permitir multiplos download
        'profile.default_content_setting_values.automatic_downloads': 1,
        # Remover todos os erros e avisos
        "excludeSwitches": ['disable-logging']
    })
    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_service.creation_flags = CREATE_NO_WINDOW
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    return driver


def digitar_naturalmente(texto, elemento):
    for letra in texto:
        elemento.send_keys(letra)
        sleep(randint(1, 5)/20)


class MagazineSpider(scrapy.Spider):
    name = "magazine"
    
    def ex_magazine(self, item_teste):

        self.item_teste1 = item_teste
        usuario = sistema.getlogin()

        os.chdir(os.path.join(os.path.expanduser('~'),'desktop'))

        if(os.path.exists('magazine.csv')):
                
            x = 0
            while True:
                if(os.path.exists(f'magazine{x}.csv')):
                    x += 1
                else:
                    arquivo1 = (f'magazine{x}.csv')
                    break

            print(f"O arquivo {arquivo1} não existe")
            ba = (f'C:/Users/{usuario}/Desktop/{arquivo1}')
            process = CrawlerProcess(settings = {'FEEDS': {arquivo1:{'format':'csv',}}})
            with open(arquivo1,"w") as arq1:
                arq1.write(self.item_teste1)
                arq1.close
            process.crawl(MagazineSpider)
            process.start()

        else:
            print("O arquivo não existe")
            ba = (f'C:/Users/{usuario}/Desktop/magazine.csv')
            process = CrawlerProcess(settings = {'FEEDS': {'magazine.csv':{'format':'csv',}}})
            with open('magazine.csv',"w") as arq1:
                arq1.write(self.item_teste1)
                arq1.close
            process.crawl(MagazineSpider)
            process.start()

    def start_requests(self):
        usuario = sistema.getlogin()

        os.chdir(os.path.join(os.path.expanduser('~'),'desktop'))

        if(os.path.exists('magazine.csv')):
                
            x = 0
            while True:
                if(os.path.exists(f'magazine{x}.csv')):
                    x += 1
                else:
                    if x == 0:
                        arquivo2 = ('magazine.csv')
                        break
                    else:
                        y = x - 1
                        arquivo2 = (f'magazine{y}.csv')
                        break
            ba = (f'C:/Users/{usuario}/Desktop/{arquivo2}')
        else:
            ba = (f'C:/Users/{usuario}/Desktop/magazine.csv')
        
        with open (arquivo2, 'r', encoding='utf-8') as arquivo:
            teste= arquivo.read()
        busque_item = teste

        self.driver = iniciar_driver()
        self.driver.get("https://www.magazineluiza.com.br/")
        sleep(5)
        campo_buscar = self.driver.find_element(By.XPATH, "//input[@id='input-search']")
        campo_buscar.click()
        sleep(1)
        digitar_naturalmente(busque_item, campo_buscar)
        sleep(2)
        campo_buscar.click()
        campo_buscar.send_keys(Keys.ENTER)
        sleep(5)
        self.driver.execute_script("window.scrollTo(0, 8000);")
        sleep(10),
        self.contagem = 2
        self.qts_paginas1 = self.driver.find_elements(By.XPATH, "//nav[@aria-label='pagination navigation']/ul/li/a")
        ultima_pagina = len(self.qts_paginas1)-1
        total_paginas = self.qts_paginas1[ultima_pagina].text
        self.total_paginas2 = int(total_paginas)+1
        sleep(5)
        self.url_inicial = self.driver.current_url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        yield scrapy.Request(url=self.url_inicial, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):
        sleep(5)
        for i in response.xpath("//li[@class='sc-ibdxON fwviCj']"):
            Titulo = i.xpath(".//h2/text()").get()
            preco1 = i.xpath(".//p[@class='sc-kDvujY jDmBNY sc-hGglLj bQqJoc']/text()").get()
            valor = str(preco1).split(';')
            preco = valor
            parcelas = i.xpath(".//p[@class='sc-kDvujY szpaO sc-kSGOQU hefOAQ']/text()[4]").get()
            juros1 = i.xpath(".//p[@class='sc-kDvujY szpaO sc-kSGOQU hefOAQ']/text()[9]").get()
            if juros1:
                juros = (f'{parcelas}x, {juros1}')
            else:
                juros = (f'Somente à vista')


            pix1 = i.xpath(".//span[2]/text()[2]").get()
            if pix1:
                pix = pix1
            else:
                pix = 'Não aceita'

            link1 = i.xpath(".//a/@href").get()
            link2 = str(link1)
            url_link = 'https://www.magazineluiza.com.br'
            link = str(f'{url_link}{link2}')


            yield {
                ' - Titulo': Titulo,
                'Preço': preco,
                'Juros': juros,
                'Pagamento por PIX': pix,
                'link': link,
            }

        if self.contagem != self.total_paginas2:
            proxima_pagima = str(f'{self.url_inicial}?page={self.contagem}')
            self.contagem += 1
            self.driver.get(proxima_pagima)
            sleep(3)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            next_page = self.driver.current_url
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)
        else:
            self.driver.close
        self.driver.close
