from time import sleep

import PySimpleGUI as sg
import wmi

from mercadolivre.mercadolivre.spiders.app import MlivreSpider
from mercadolivre.mercadolivre.spiders.app1 import ShopeeSpider
from mercadolivre.mercadolivre.spiders.app2 import AmazonSpider
from mercadolivre.mercadolivre.spiders.app3 import MagazineSpider
from mercadolivre.mercadolivre.spiders.app4 import AmericanasSpider
from mercadolivre.mercadolivre.spiders.go_she import GoogleSheets

sg.theme('PythonPlus')

def pagina_conectando():
    font = ('Arial Baltic', 16)
    layout = [
        [sg.Text('')],
        [sg.Text('Conectar ao servidor', font=30, key='-CONEX-')],
        [sg.Text('')],
        [sg.ProgressBar(max_value=100, orientation='h',size=(30,15),key='-PROG1-', bar_color='#C0C0C0')],
        [sg.Text('')],
        [sg.Text('', key='-CONEX1-')],
        [sg.Text('')],
        [sg.Button('CONECTAR', font=25, size=(12, 2), button_color=('#ffffff', '#b5b3af'))],
        [sg.Text('')]
    ]
    return sg.Window('Fevox Conectar',icon='logo_fevox.ico',size=(400,330), element_justification='center', layout=layout, finalize=True)

def pagina_popup1():
    layout = [
        [sg.Text('')],
        [sg.Text('ATENÇÃO!!!!', font=30)],
        [sg.Text('')],
        [sg.Text('Acesso Negado!')],
        [sg.Text('', key='-ERRO-')],
        [sg.Text('Entrar em contato pelo telefone:')],
        [sg.Text('(11) 97826-4735')],
        [sg.Text('')]
    ]
    return sg.Window('Fevox Erro',icon='logo_fevox.ico',size=(250,220), element_justification='center', layout=layout, finalize=True)

def pagina_inicial():
    font = ('Arial Baltic', 16)
    layout = [
        [sg.Text('')],
        [sg.Text('Em qual site?', font=30)],
        [sg.Text('')],
        [sg.Radio('MERCADO LIVRE', group_id='tipo_site', key='MERCADO LIVRE', font=font)],
        [sg.Radio('SHOPEE', group_id='tipo_site', key='SHOPEE', font=font)],
        [sg.Radio('AMAZON', group_id='tipo_site', key='AMAZON', font=font)],
        [sg.Radio('MAGAZINE LUIZA', group_id='tipo_site', key='MAGAZINE LUIZA', font=font)],
        [sg.Radio('AMERICANAS', group_id='tipo_site', key='AMERICANAS', font=font)],
        [sg.Text('')],
        [sg.Button('INICIAR', font=25, size=(8, 2), button_color=('#ffffff', '#b5b3af'))],
        [sg.Text('')]
    ]
    return sg.Window('Fevox Pesquisa',icon='logo_fevox.ico',size=(400,400), element_justification='center', layout=layout, finalize=True)


def pagina_dois(item_escolhido):
    font = ('Arial Baltic', 16)
    layout = [
        [sg.Text(f'Busca pelo site', font=30)],
        [sg.Text(f'{item_escolhido}', font=30)],
        [sg.Text('')],
        [sg.Text('Insira abaixo', font=font)],
        [sg.Text('Item a ser pesquisado', font=20)],
        [sg.Text('')],
        [sg.Input(key='item_a_ser_buscado', size=(100,20), background_color='#ffffff', text_color='#000000', font=10)],
        [sg.Text(key='status_licenca')],
        [sg.Button('Voltar', font=25, size=(8, 2), button_color=('#ffffff', '#b5b3af')), sg.Button('Próximo', font=25, size=(8, 2),button_color=('#ffffff', '#b5b3af'))],
        [sg.Text('')]
    ]
    return sg.Window('Fevox Item',icon='logo_fevox.ico',size=(400,330), element_justification='center', layout=layout, finalize=True)


def pagina_tres(item1,item2,item3, link_passado):
    layout = [
        [sg.Text(f'Iniciar busca pelo site', font=30)],
        [sg.Text(f'{item_escolhido}', font=30)],
        [sg.Text('')],
        [sg.Text(f'{item1}', font=20)],
        [sg.Text(f'{item2}', font=20)],
        [sg.Text(f'{item3}', font=20)],
        [sg.Text('')],
        [sg.Button('Voltar', font=25, size=(8, 2), button_color=('#ffffff', '#b5b3af')), sg.Button('Buscar', font=25, size=(8, 2),button_color=('#ffffff', '#b5b3af'))],
        [sg.Text('')]
    ]
    return sg.Window('Fevox Confirmação',icon='logo_fevox.ico',size=(800,330), element_justification='center', layout=layout, finalize=True)


def pagina_quatro():
    layout = [
        [sg.Text('')],
        [sg.Text('Finalizando busca no site', font=30)],
        [sg.Text('')],
        [sg.Text(f'{item_escolhido}', font=30)],
        [sg.Text('AGUARDE...', font=30)],
        [sg.Text('')],
        [sg.ProgressBar(max_value=100, orientation='h',size=(30,15),key='-PROG-')],
        [sg.Text('')],
        [sg.Text('', key='-Aguarde-')],
        [sg.Text('')]
    ]
    return sg.Window('Fevox Realizando Busca',icon='logo_fevox.ico',size=(400,330), element_justification='center', layout=layout, finalize=True)

pagina_conectando_, pagina_popup1_, pagina_inicial_, pagina_dois_, pagina_tres_, pagina_quatro_ = pagina_conectando(), None, None, None, None, None

item_escolhido = ''
while True:
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED:
        break
    elif window == pagina_conectando_:
        pc = wmi.WMI()
        os_info = pc.Win32_OperatingSystem()[0]
        teste = str(os_info)
        arq_teste = (teste).split(';')
        for x in arq_teste:
            palavra = "SerialNumber"
            if palavra not in x:
                pass
            else:
                number = (x).split('"')
                serial_number = number[1]

        if event == 'CONECTAR':
            pagina_conectando_['-CONEX-'].update('Aguarde a conexão', font=30)
            google_sheets_api = GoogleSheets()
            teste = google_sheets_api.exibir_bloqueados('IP Mac')
            ip_local = serial_number
            # ip_local = '011111'
            nome_atual = 'Eudes Pessoa'
            email_atual = 'eudesfernandapessoa_testando123@gmail.com'

            bloquear = ''
            user = nome_atual
            pagina_conectando_['-CONEX1-'].update(f'user: {user}', font=30)
            for i in range(100):
                event = window.read(timeout=1)
                pagina_conectando_['-PROG1-'].update(bar_color=('#FFFFFF','#C0C0C0'))
                pagina_conectando_['-PROG1-'].update(i+1)
                sleep(0.1)

            bloqueado = ' '
            valor_celular = 2
            for x in teste:
                y = str(x).replace('[','').replace(']','').replace("'","")
                if y == ip_local:
                    bloqueado = 'sim'
                    valor_celular += 1
                    break
                else:
                    bloqueado = 'não'
                    valor_celular += 1

            if bloqueado == 'sim':
                bloquear = 'ip'

            else:
                teste1 = google_sheets_api.exibir_relatorio('IP Mac')
                valor_celular = 2
                ip_cadastrado = 'não'
                email_cadastrado = 'não'
                email_conferir = ''
                for x in teste1:
                    y = str(x).replace('[','').replace(']','').replace("'","")
                    if y == ip_local:
                        teste2 = google_sheets_api.exibir_relatorio('Pagamento Efetuado', valor_celular-2)
                        if teste2 == 'sim':
                            teste3 = google_sheets_api.exibir_relatorio('Email', valor_celular-2)
                            if teste3 == email_atual:
                                ip_cadastrado = 'sim'
                                email_cadastrado = 'sim'

                            elif teste3 != email_atual:
                                ip_cadastrado = 'sim'
                                email_cadastrado = 'sim'
                                bloquear = 'email'

                        else:
                            ip_cadastrado = 'sim' 
                            email_cadastrado = 'não'
                            valor_celular += 1
                            bloquear = 'pagamaneto'

                    else:
                        valor_celular += 1

                valor_celula1 = 2
                for x in teste1:
                    teste4 = google_sheets_api.exibir_relatorio('Email', valor_celula1-2)
                    y = str(teste4).replace('[','').replace(']','').replace("'","")
                    if y == email_atual:
                        email_cadastrado = 'sim'
                    else:
                        valor_celula1 += 1

                if ip_cadastrado == 'não' and email_cadastrado == 'sim':
                    google_sheets_api.inserir_bloqueado(nome=nome_atual, email=email_atual, ip_atual=ip_local)
                    bloquear = 'ip'
                elif ip_cadastrado == 'sim' and email_cadastrado == 'não':
                    pass
                elif ip_cadastrado == 'não' and email_cadastrado == 'não':
                    google_sheets_api.inserir_entrada(nome=nome_atual, email=email_atual, ip_atual=ip_local, status_pagamento='sim')

        if bloquear == 'ip':
            pagina_conectando_.hide()
            pagina_popup1_ = pagina_popup1()
            pagina_popup1_['-ERRO-'].update('Erro: 01', font=30)
            if window == pagina_popup1_:
                if event == sg.WIN_CLOSED:
                    break
        elif bloquear == 'email':
            pagina_conectando_.hide()
            pagina_popup1_ = pagina_popup1()
            pagina_popup1_['-ERRO-'].update('Erro: 02', font=30)
            if window == pagina_popup1_:
                if event == sg.WIN_CLOSED:
                    break
        elif bloquear == 'pagamaneto':
            pagina_conectando_.hide()
            pagina_popup1_ = pagina_popup1()
            pagina_popup1_['-ERRO-'].update('Erro: 03', font=30)
            if window == pagina_popup1_:
                if event == sg.WIN_CLOSED:
                    break
        else:
            pagina_conectando_.close()
            pagina_inicial_ = pagina_inicial()

    elif window == pagina_inicial_:
        if event == 'INICIAR':
            for x, y in values.items():
                if y is True:
                    item_escolhido = x
                    pagina_inicial_.hide()
                    pagina_dois_ = pagina_dois(item_escolhido)

    elif window == pagina_dois_:
        if event == 'Voltar':
            pagina_inicial_.un_hide()
            pagina_dois_.hide()
        elif event == 'Próximo':
            if values['item_a_ser_buscado']:
                item1 = values['item_a_ser_buscado'][0:70]
                item2 = values['item_a_ser_buscado'][70:140]
                item3 = values['item_a_ser_buscado'][140:280]

                if item_escolhido == 'MERCADO LIVRE':
                    link_passado = values['item_a_ser_buscado']
                    pagina_tres_ = pagina_tres(item1,item2,item3, link_passado)
                    pagina_dois_.hide()

                elif item_escolhido == 'SHOPEE':
                    link_passado = values['item_a_ser_buscado']
                    pagina_tres_ = pagina_tres(item1,item2,item3, link_passado)
                    pagina_dois_.hide()

                elif item_escolhido == 'AMAZON':
                    link_passado = values['item_a_ser_buscado']
                    pagina_tres_ = pagina_tres(item1,item2,item3, link_passado)
                    pagina_dois_.hide()

                elif item_escolhido == 'MAGAZINE LUIZA':
                    link_passado = values['item_a_ser_buscado']
                    pagina_tres_ = pagina_tres(item1,item2,item3, link_passado)
                    pagina_dois_.hide()

                elif item_escolhido == 'AMERICANAS':
                    link_passado = values['item_a_ser_buscado']
                    pagina_tres_ = pagina_tres(item1,item2,item3, link_passado)
                    pagina_dois_.hide()
                    
            else:
                pagina_dois_[
                    'status_licenca'].update(text_color='red')
                pagina_dois_[
                    'status_licenca'].update('Digitar item', font=10)

    elif window == pagina_tres_:
        if event == 'Voltar':
            pagina_dois_.un_hide()
            pagina_tres_.hide()
    
        elif event == 'Buscar':

            if item_escolhido == 'MERCADO LIVRE':
                pagina_quatro_ = pagina_quatro()
                pagina_tres_.hide()
                item_buscar = link_passado
                exe_ml = MlivreSpider()
                exe_ml.ex_mercadolivre(item_teste=item_buscar)
                for i in range(100):
                    event = window.read(timeout=1)
                    pagina_quatro_['-PROG-'].update(bar_color=('#FFFF00','#00008B'))
                    pagina_quatro_['-PROG-'].update(i+1)
                    pagina_quatro_['-Aguarde-'].update('Ao finalizar ele fechará sozinho', font=10)
                    sleep(0.1)
                pagina_inicial_.close()
                pagina_dois_.close()
                pagina_tres_.close()
                pagina_quatro_.close()  
                break

            elif item_escolhido == 'SHOPEE':
                pagina_quatro_ = pagina_quatro()
                pagina_tres_.hide()
                item_buscar = link_passado
                exe_shopee = ShopeeSpider()
                exe_shopee.ex_shopee(item_teste=item_buscar)
                for i in range(100):
                    event = window.read(timeout=1)
                    pagina_quatro_['-PROG-'].update(bar_color=('#FF4500','#ffffff'))
                    pagina_quatro_['-PROG-'].update(i+1)
                    pagina_quatro_['-Aguarde-'].update('Ao finalizar ele fechará sozinho', font=10)
                    sleep(0.1)
                pagina_inicial_.close()
                pagina_dois_.close()
                pagina_tres_.close()
                pagina_quatro_.close()  
                break

            elif item_escolhido == 'AMAZON':
                pagina_quatro_ = pagina_quatro()
                pagina_tres_.hide()
                item_buscar = link_passado
                exe_amazon = AmazonSpider()
                exe_amazon.ex_amazom(item_teste=item_buscar)
                for i in range(100):
                    event = window.read(timeout=1)
                    pagina_quatro_['-PROG-'].update(bar_color=('#FF8C00','#00008B'))
                    pagina_quatro_['-PROG-'].update(i+1)
                    pagina_quatro_['-Aguarde-'].update('Ao finalizar ele fechará sozinho', font=10)
                    sleep(0.1)
                pagina_inicial_.close()
                pagina_dois_.close()
                pagina_tres_.close()
                pagina_quatro_.close()  
                break

            elif item_escolhido == 'MAGAZINE LUIZA':
                pagina_quatro_ = pagina_quatro()
                pagina_tres_.hide()
                item_buscar = link_passado
                exe_maganize = MagazineSpider()
                exe_maganize.ex_magazine(item_teste=item_buscar)
                for i in range(100):
                    event = window.read(timeout=1)
                    pagina_quatro_['-PROG-'].update(bar_color=('#0484fc','#ffffff'))
                    pagina_quatro_['-PROG-'].update(i+1)
                    pagina_quatro_['-Aguarde-'].update('Ao finalizar ele fechará sozinho', font=10)
                    sleep(0.1)
                pagina_inicial_.close()
                pagina_dois_.close()
                pagina_tres_.close()
                pagina_quatro_.close()  
                break

            elif item_escolhido == 'AMERICANAS':
                pagina_quatro_ = pagina_quatro()
                pagina_tres_.hide()
                item_buscar = link_passado
                exe_maganize = AmericanasSpider()
                exe_maganize.ex_americanas(item_teste=item_buscar)
                for i in range(100):
                    event = window.read(timeout=1)
                    pagina_quatro_['-PROG-'].update(bar_color=('#f80032','#ffffff'))
                    pagina_quatro_['-PROG-'].update(i+1)
                    pagina_quatro_['-Aguarde-'].update('Ao finalizar ele fechará sozinho', font=10)
                    sleep(0.1)
                pagina_inicial_.close()
                pagina_dois_.close()
                pagina_tres_.close()
                pagina_quatro_.close()  
                break

                    