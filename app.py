import os
import os as sistema
from random import randint
from subprocess import CREATE_NO_WINDOW
from time import sleep

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.support import expected_conditions as CondicaoExperada
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


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
        # Remover todos os erros e avisos, 
        "excludeSwitches": ['disable-logging'],
        
    })
    chrome_service = ChromeService(ChromeDriverManager().install())
    chrome_service.creation_flags = CREATE_NO_WINDOW
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    return driver


def digitar_naturalmente(texto, elemento):
    for letra in texto:
        elemento.send_keys(letra)
        sleep(randint(1, 5)/20)


class MlivreSpider(scrapy.Spider):
    name = "mlivre"

    def ex_mercadolivre(self, item_teste):
        self.item_teste1 = item_teste
        usuario = sistema.getlogin()

        os.chdir(os.path.join(os.path.expanduser('~'),'desktop'))

        if(os.path.exists('mercadolivre.csv')):
                
            x = 0
            while True:
                if(os.path.exists(f'mercadolivre{x}.csv')):
                    x += 1
                else:
                    arquivo1 = (f'mercadolivre{x}.csv')
                    break

            ba = (f'C:/Users/{usuario}/Desktop/{arquivo1}')
            process = CrawlerProcess(settings = {'FEEDS': {arquivo1:{'format':'csv',}}})
            with open(arquivo1,"w") as arq1:
                arq1.write(self.item_teste1)
                arq1.close
            process.crawl(MlivreSpider)
            process.start()

        else:
            ba = (f'C:/Users/{usuario}/Desktop/mercadolivre.csv')
            process = CrawlerProcess(settings = {'FEEDS': {'mercadolivre.csv':{'format':'csv',}}})
            with open('mercadolivre.csv',"w") as arq1:
                arq1.write(self.item_teste1)
                arq1.close
            process.crawl(MlivreSpider)
            process.start()

    def start_requests(self):
        usuario = sistema.getlogin()

        os.chdir(os.path.join(os.path.expanduser('~'),'desktop'))

        if(os.path.exists('mercadolivre.csv')):
                
            x = 0
            while True:
                if(os.path.exists(f'mercadolivre{x}.csv')):
                    x += 1
                else:
                    if x == 0:
                        arquivo2 = ('mercadolivre.csv')
                        break
                    else:
                        y = x - 1
                        arquivo2 = (f'mercadolivre{y}.csv')
                        break
            ba = (f'C:/Users/{usuario}/Desktop/{arquivo2}')
        else:
            ba = (f'C:/Users/{usuario}/Desktop/mercadolivre.csv')
        
        with open (arquivo2, 'r', encoding='utf-8') as arquivo:
            teste= arquivo.read()
        busque_item = teste

        self.driver = iniciar_driver()
        self.driver.get("https://www.mercadolivre.com.br/")
        sleep(5)
        campo_buscar = self.driver.find_element(By.XPATH, "//input[@id='cb1-edit']")
        campo_buscar.click()
        sleep(1)
        digitar_naturalmente(busque_item, campo_buscar)
        sleep(2)
        btn_procurar = self.driver.find_element(By.XPATH, "//button[@class='nav-search-btn']")
        sleep(3)
        btn_procurar.click()
        sleep(10)
        url_inicial = self.driver.current_url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        yield scrapy.Request(url=url_inicial, headers=self.headers, callback=self.parse)

    def parse(self, response, **kwargs):
        for i in response.xpath("//section[@class='ui-search-results ui-search-results--without-disclaimer shops__search-results']//ol/li"):
            Titulo = i.xpath(".//h2/text()").get()
            preco1 = i.xpath(".//span[@class='price-tag ui-search-price__part shops__price-part']//text()").getall()
            numero_itens_valor = int(len(preco1))
            if numero_itens_valor < 4:
                preco_sim = 1
            elif numero_itens_valor >= 4:
                preco_sim = 2

            if preco_sim == 2:
                if preco1[4] == 'R$':
                    preco1[4] = '00'
                    valor = str(preco1[2]).replace('.', '')
                    preco = (f'{valor}.{preco1[4]}')
                else:
                    valor = str(preco1[2]).replace('.', '')
                    preco = (f'{valor}.{preco1[4]}')

                juros1 = i.xpath(".//span[@class='ui-search-item__group__element shops__items-group-details ui-search-installments ui-search-color--LIGHT_GREEN']/text()").getall()
                if juros1:
                    juros = juros1
                else:
                    juros2 = i.xpath(".//span[@class='ui-search-item__group__element shops__items-group-details ui-search-installments ui-search-color--BLACK']/text()").getall()
                    juros3 = str(juros2).replace('[','').replace(']','').replace("'","")
                    juros = f'{juros3} ,Com juros'

                frete_gratis1 = i.xpath(".//p[@class='ui-search-item__shipping ui-search-item__shipping--free shops__item-shipping-free']/text()").get()
                if frete_gratis1 == 'Frete grátis':
                    frete_gratis = 'Sim'
                else:
                    frete_gratis = 'Não'
                full1 = i.xpath(".//span[@class='ui-search-item__fulfillment']").get()
                if full1:
                    full = 'Sim'
                else:
                    full = 'Não'
                link = i.xpath(".//a/@href").get()
                
                yield {
                    ' - Titulo': Titulo,
                    'Preco': preco,
                    'Juros': juros,
                    'Frete_Gratis': frete_gratis,
                    'Full': full,
                    'link': link
                }
            
            elif preco_sim == 1:
                valor = str(preco1[2]).replace('.', '')
                preco = (f'{valor}.00')

                juros = 'Sem opção'
                frete_gratis = 'Não'
                full = 'Não'
                link = i.xpath(".//a/@href").get()

                yield {
                    ' - Titulo': Titulo,
                    'Preco': preco,
                    'Juros': juros,
                    'Frete_Gratis': frete_gratis,
                    'Full': full,
                    'link': link
                }


        next_page = response.xpath("//li[@class='andes-pagination__button andes-pagination__button--next shops__pagination-button']/a/@href").get()
        if next_page:
            self.driver.get(next_page)
            sleep(5)
            proxima_pagima = self.driver.current_url
            yield scrapy.Request(url=proxima_pagima, headers=self.headers, callback=self.parse)
