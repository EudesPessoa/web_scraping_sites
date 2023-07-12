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
import math

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


class AmericanasSpider(scrapy.Spider):
    name = "americanas"
    
    def ex_americanas(self, item_teste):

        self.item_teste1 = item_teste
        usuario = sistema.getlogin()

        os.chdir(os.path.join(os.path.expanduser('~'),'desktop'))

        if(os.path.exists('americanas.csv')):
                
            x = 0
            while True:
                if(os.path.exists(f'americanas{x}.csv')):
                    x += 1
                else:
                    arquivo1 = (f'americanas{x}.csv')
                    break

            print(f"O arquivo {arquivo1} não existe")
            ba = (f'C:/Users/{usuario}/Desktop/{arquivo1}')
            process = CrawlerProcess(settings = {'FEEDS': {arquivo1:{'format':'csv',}}})
            with open(arquivo1,"w") as arq1:
                arq1.write(self.item_teste1)
                arq1.close
            process.crawl(AmericanasSpider)
            process.start()

        else:
            print("O arquivo não existe")
            ba = (f'C:/Users/{usuario}/Desktop/americanas.csv')
            process = CrawlerProcess(settings = {'FEEDS': {'americanas.csv':{'format':'csv',}}})
            with open('americanas.csv',"w") as arq1:
                arq1.write(self.item_teste1)
                arq1.close
            process.crawl(AmericanasSpider)
            process.start()

    def start_requests(self):
        usuario = sistema.getlogin()

        os.chdir(os.path.join(os.path.expanduser('~'),'desktop'))

        if(os.path.exists('americanas.csv')):
                
            x = 0
            while True:
                if(os.path.exists(f'americanas{x}.csv')):
                    x += 1
                else:
                    if x == 0:
                        arquivo2 = ('americanas.csv')
                        break
                    else:
                        y = x - 1
                        arquivo2 = (f'americanas{y}.csv')
                        break
            ba = (f'C:/Users/{usuario}/Desktop/{arquivo2}')
        else:
            ba = (f'C:/Users/{usuario}/Desktop/americanas.csv')
        
        with open (arquivo2, 'r', encoding='utf-8') as arquivo:
            teste= arquivo.read()
        busque_item = teste

        self.driver = iniciar_driver()
        self.driver.get("https://www.americanas.com.br/")
        sleep(5)
        campo_buscar = self.driver.find_element(By.XPATH, "//input[@placeholder='busque aqui seu produto']")
        campo_buscar.click()
        sleep(1)
        digitar_naturalmente(busque_item, campo_buscar)
        sleep(2)
        campo_buscar.click()
        campo_buscar.send_keys(Keys.ENTER)
        sleep(5)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(10)
        self.qts_produtos = self.driver.find_elements(By.XPATH, "//div[@class='col__StyledCol-sc-1snw5v3-0 exNZoL full-grid__ColTop-sc-19t7jwc-10 jNhMOH']/span")
        self.div_produtos = int(self.qts_produtos[0].text.split(' ')[0])/24
        self.total_produtos = int(self.qts_produtos[0].text.split(' ')[0])
        self.qts_paginas = math.ceil(self.div_produtos)
        sleep(5)
        self.contagem = 1
        self.num_item_pagina = 24
        self.url_inicial = self.driver.current_url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        yield scrapy.Request(url=self.url_inicial, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):
        sleep(5)
        for i in response.xpath("//div[@class='col__StyledCol-sc-1snw5v3-0 bIoTYC full-grid__ColUI-sc-19t7jwc-9 iIVCOo']/div[2]/div"):
            Titulo = i.xpath(".//a/div[2]//h3/text()").get()
            preco1 = i.xpath(".//a/div[3]/span[1]/text()").get()
            parcelas = i.xpath(".//a/div[3]/span[2]/text()").get()


            frete_gratis = i.xpath(".//div[@class='freight-tag__DeliveryBadge-sc-1q1utxk-0 hYGrZr']/text()").get()
            if frete_gratis:
                pix = frete_gratis
            else:
                pix = 'Não aceita'

            link1 = i.xpath(".//a/@href").get()
            link2 = str(link1)
            url_link = 'https://www.americanas.com.br'
            link = str(f'{url_link}{link2}')


            yield {
                ' - Titulo': Titulo,
                'Preço': preco1,
                'Juros': parcelas,
                'Frete Gratis': pix,
                'link': link,
            }

        if self.contagem != self.qts_paginas+1:
            if self.num_item_pagina >= self.total_produtos:
                self.num_item_pagina = self.total_produtos
            else:
                pass
            proxima_pagima = str(f'{self.url_inicial}?limit=24&offset={self.num_item_pagina}')
            self.contagem += 1
            self.num_item_pagina += 24
            self.driver.get(proxima_pagima)
            sleep(3)
            next_page = self.driver.current_url
            yield scrapy.Request(url=next_page, headers=self.headers, callback=self.parse)
        else:
            self.driver.close
        self.driver.close
