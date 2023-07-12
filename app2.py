import scrapy
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from time import sleep
from random import randint
import re
from scrapy.crawler import CrawlerProcess
import os as sistema
import os
from subprocess import CREATE_NO_WINDOW


def iniciar_driver():
    chrome_options = Options()

    arguments = ['--lang=pt-BR', '--window-size=1300,1000', '--incognito',  ]

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


class AmazonSpider(scrapy.Spider):
    name = "amazon"

    def ex_amazom(self, item_teste):
        self.item_teste1 = item_teste
        usuario = sistema.getlogin()

        os.chdir(os.path.join(os.path.expanduser('~'),'desktop'))

        if(os.path.exists('amazon.csv')):
                
            x = 0
            while True:
                if(os.path.exists(f'amazon{x}.csv')):
                    x += 1
                else:
                    arquivo1 = (f'amazon{x}.csv')
                    break

            print(f"O arquivo {arquivo1} não existe")
            ba = (f'C:/Users/{usuario}/Desktop/{arquivo1}')
            process = CrawlerProcess(settings = {'FEEDS': {arquivo1:{'format':'csv',}}})
            with open(arquivo1,"w") as arq1:
                arq1.write(self.item_teste1)
                arq1.close
            process.crawl(AmazonSpider)
            process.start()

        else:
            print("O arquivo não existe")
            ba = (f'C:/Users/{usuario}/Desktop/amazon.csv')
            process = CrawlerProcess(settings = {'FEEDS': {'amazon.csv':{'format':'csv',}}})
            with open('amazon.csv',"w") as arq1:
                arq1.write(self.item_teste1)
                arq1.close
            process.crawl(AmazonSpider)
            process.start()

    def start_requests(self):
        usuario = sistema.getlogin()

        os.chdir(os.path.join(os.path.expanduser('~'),'desktop'))

        if(os.path.exists('amazon.csv')):
                
            x = 0
            while True:
                if(os.path.exists(f'amazon{x}.csv')):
                    x += 1
                else:
                    if x == 0:
                        arquivo2 = ('amazon.csv')
                        break
                    else:
                        y = x - 1
                        arquivo2 = (f'amazon{y}.csv')
                        break
            ba = (f'C:/Users/{usuario}/Desktop/{arquivo2}')
        else:
            ba = (f'C:/Users/{usuario}/Desktop/amazon.csv')
        
        with open (arquivo2, 'r', encoding='utf-8') as arquivo:
            teste= arquivo.read()
        busque_item = teste

        self.driver = iniciar_driver()
        self.driver.get("https://www.amazon.com.br/")
        sleep(5)
        campo_buscar = self.driver.find_element(By.XPATH, "//input[@id='twotabsearchtextbox']")
        campo_buscar.click()
        sleep(1)
        digitar_naturalmente(busque_item, campo_buscar)
        sleep(2)
        btn_procurar = self.driver.find_element(By.XPATH, "//input[@id='nav-search-submit-button']")
        sleep(2)
        btn_procurar.click()
        sleep(3)
        url_inicial = self.driver.current_url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        yield scrapy.Request(url=url_inicial, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):
        for i in response.xpath("//div[@class='sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20']"):
            Titulo = i.xpath(".//h2/a/span/text()").get()
            preco1 = i.xpath(".//span[@class='a-price']/span[@class='a-offscreen']/text()").get()
            valor1 = str(preco1).replace('.', '').replace('R$','')
            valor = str(valor1).replace(',', '.').split()
            preco = (valor)

            juros1 = i.xpath(".//div[@class='a-row a-size-base a-color-base']//text()").getall()
            juros2= str(juros1)
            lista = []
            item = re.compile(r'em até..x')
            resultado = item.findall(juros2)
            result = str(resultado).replace('[','').replace(']','')
            item1 = re.compile(r'em até...x')
            resultado1 = item1.findall(juros2)
            result1 = str(resultado1).replace('[','').replace(']','')
            item2 = re.compile(r'....juros')
            resultado2 = item2.findall(juros2)
            result2 = str(resultado2).replace('[','').replace(']','')
            if resultado:
                lista.append(f'{result} {result2}')
            elif resultado1:
                lista.append(f'{result1} {result2}')
            else:
                lista.append(f'Poduto não parcela')

            frete = i.xpath(".//span[@class='a-color-base']/text()").getall()
            frete1 = str(frete)
            lista1 = []
            item = re.compile(r'Opção de frete GRÁTIS disponível')
            resultado = item.findall(frete1)
            result = str(resultado).replace('[','').replace(']','')
            item1 = re.compile(r'Frete GRÁTIS')
            resultado1 = item1.findall(frete1)
            result1 = str(resultado1).replace('[','').replace(']','')
            item2 = re.compile(r'.......de frete')
            resultado2 = item2.findall(frete1)
            result2 = str(resultado2).replace('[','').replace(']','')
            if resultado:
                lista1.append(f'{result}')
            elif resultado1:
                lista1.append(f'{result1}')
            else:
                lista1.append(f'{result2}')

            link1 = i.xpath(".//span[@class='rush-component']/a/@href").get()
            link2 = str(link1)
            url_link = 'https://www.amazon.com.br'
            link = str(f'{url_link}{link2}')

            yield {
                ' - Titulo': Titulo,
                'Preco': preco,
                'Juros': lista,
                'Frete Gratis': lista1,
                'link': link
            }

        next_page = response.xpath("//span[@class='s-pagination-strip']/a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']/@href").get()
        next_page1 = str(next_page)
        next_page_proximo = str(f'{url_link}{next_page1}')
        if next_page:
            self.driver.get(next_page_proximo)
            sleep(5)
            proxima_pagima = self.driver.current_url
            yield scrapy.Request(url=proxima_pagima, headers=self.headers, callback=self.parse)
        else:
            self.driver.close
        self.driver.close
