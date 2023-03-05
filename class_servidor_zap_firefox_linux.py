class servidor_zap:
    def __init__(self,id_user='1',id_sessao='1',status_arquivo=False,backend=True):
        #caminho perfil horiginal"/home/administrador/.mozilla/firefox/fpmm6lyy.default-release"

        self.mensagens=[
            ['999999999','ola boot teste 1'],
            ['nome ou telefone'],
        ]

        self.mensagem=["bom dia","Teste boot"]
        self.status_arquivo=status_arquivo



        import os #para diretorios

        from selenium import webdriver #para automacao

        from selenium.webdriver.common.keys import Keys #para interação tag
        from selenium.webdriver.common.by import By #para seletores "identificar"
        from selenium.webdriver.common.action_chains import ActionChains  #alternativa ao send_keys
        import time

        from selenium.webdriver.firefox.options import Options #opções firefox


        self.os=os

        self.webdriver=webdriver

        self.By=By
        self.Keys=Keys
        self.ActionChains=ActionChains
        self.time=time


        self.Options=Options
        self.options = Options()


        #definindo diretorios
        self.dir_raiz = os.getcwd()
        dir_sessao=self.def_barramento([self.dir_raiz, 'sessao', 'id_user'+id_user, 'id_sessao'+id_sessao])
        dir_driver=self.def_barramento([self.dir_raiz, 'driver', driver])


        self.dir_navegador=self.def_barramento([dir_sessao, 'firefox'])
        if self.os.path.isdir(self.dir_navegador) == False :
            self.os.makedirs(self.dir_navegador)


        if status_arquivo == True:
            self.dir_sessao={
                'mensagem':self.def_barramento([dir_sessao, 'status_msg.txt']),
                'qrcod':self.def_barramento([dir_sessao, 'status_qrcod.txt'])
            }

        else:
            self.dir_sessao={
                'mensagem':'',
                'qrcod':''
            }


        print("Diretorio do perfil : "+self.dir_navegador)

        self.options.headless = backend

        self.get_perfil()

    #/////////////////////////////////////////////////////////////////////////////
    def get_perfil(self):
        print('abrindo pagina ....')
        sessao_firefox = self.webdriver.FirefoxProfile(rf""+self.dir_navegador)
        self.browser = self.webdriver.Firefox( options=self.options,firefox_profile=sessao_firefox)#service=dir_driver,
        self.browser.get("about:support")

        start =1
        while start !=0 :
            self.time.sleep(1)
            dir_temp=self.atributo_get('[id="profile-dir-box"]','html')
            if dir_temp !=False:
                start =0
        self.dir_temp=dir_temp
        #print("Diretorio temporario "+dir_temp)

        self.time.sleep(1)

        self.atributo_set('[body]','control','t')
        self.browser.get("https://web.whatsapp.com")
        #self.actions = self.ActionChains(self.browser)


    #/////////////////////////////////////////////////////////////////////////////
    def set_perfil(self):
        print('salvando perfil...')

        files = self.os.listdir(self.dir_temp)
        #print(files)
        #self.shutil.copytree(self.dir_temp, self.dir_navegador)
        self.os.system('rm -r '+self.dir_navegador)
        #self.os.system('mkdir '+self.dir_navegador)
        if self.os.path.isdir(self.dir_navegador) == False :
            self.os.makedirs(self.dir_navegador)

        for f in files:
            #self.copyfile(self.dir_temp+'/'+f,self.dir_navegador)
            self.os.system("cp -r "+self.dir_temp+'/'+f+' '+self.dir_navegador)

    #/////////////////////////////////////////////////////////////////////////////
    def def_barramento(self,diretorio=['c:','pasta']):
        return  '/'.join(diretorio)
    #////////////////////////////////////////////////////////////////////////////
    def atributo_existe(self,atributo,valor):
        re=self.browser.find_elements(self.By.CSS_SELECTOR, '['+atributo+'="'+valor+'"]')
        if len(re) > 0:
            return '1'
        else:
            return '0'
    #/////////////////////////////////////////////////////////////////////////////
    def atributo_get(self,nome_seletor,atributo):
        re=self.browser.find_elements(self.By.CSS_SELECTOR, nome_seletor)
        if len(re) > 0:
            if atributo == 'html':
                return re[0].text
            else:
                return re[0].get_attribute(atributo)
        else:
            return False
    #/////////////////////////////////////////////////////////////////////////////
    def tag(self,nome_seletor):
        re=self.browser.find_elements(self.By.CSS_SELECTOR, nome_seletor)
        if len(re) > 0:
            return re[0]
        else:
            return False
    #/////////////////////////////////////////////////////////////////////////////
    def tag_set(self,tag,tipo="text",texto=""):

        actions = self.ActionChains(self.browser)
        #actions.move_to_element(bnt1).send_keys(msg_glo + self.Keys.ENTER).perform()
        if tipo == 'click':
            #tag.click()
            actions.move_to_element(tag).click().perform()
            return True
        elif tipo == 'text':
            #tag.send_keys(texto)
            actions.move_to_element(tag).send_keys(texto).perform()
            return True
        elif tipo == 'enter':
            actions.move_to_element(tag).send_keys(self.Keys.ENTER).perform()
            return True
        elif tag == 'control':
            actions.move_to_element(tag).send_keys(self.Keys.CONTROL + texto).perform()
            return True
        else:
            actions.move_to_element(tag).send_keys(tipo).perform()
            return True
    #/////////////////////////////////////////////////////////////////////////////
    def tag_get(self,tag,atributo=False):
        if atributo == False:
            return tag.text
        else:
            return tag.get_attribute(atributo)
    #/////////////////////////////////////////////////////////////////////////////
    def atributo_set(self,nome_seletor,atributo=False,texto=False,espera=0):
        #re='lixo'
        #del re
        re=self.browser.find_elements(self.By.CSS_SELECTOR, nome_seletor)



        if len(re) > 0:
            if atributo == 'click':
                re[0].click()
                saida=True
            elif texto != False and atributo == 'enter':


                re[0].send_keys(texto)

                self.time.sleep(espera);
                re[0].send_keys(self.Keys.ENTER)
                saida = True

            elif texto != False and atributo == 'control':

                re[0].send_keys(Keys.CONTROL + texto)
                saida = True

            else:

                return re[0]

            return saida
        else:
            return False

    #///////////////////////////////////////////////////////////////////////////////
    def dados_login(self):
        if self.atributo_set('[class="_3g4Pn _2HcPg"]','click') != False:

            self.time.sleep(3)
            foto=self.atributo_get('[style="height: 100%; width: 100%; visibility: visible;"]','src')

            self.time.sleep(3)
            nome=self.atributo_get('[data-testid="col-main-profile-input"]','html')


        else :
            foto ='false'
            nome ='false'
        self.loop_text=self.loop_text+foto+'<_>'+nome+'<_>'
        print('Nome : '+nome)
        self.time.sleep(3)

    #///////////////////////////////////////////////////////////////////////////////
    def status_pagina(self):

        log=self.atributo_existe('data-testid','icon-search-morph')
        qrcod=self.atributo_existe('data-testid','qrcode')
        val=self.status[log+'_'+qrcod];
        self.loop_print=val['print']
        self.loop_start=val['loop']
        self.loop_text=val['text']
        #return self.status[log+'_'+qrcod];
    #//////////////////////////////////////////////////////////////////////////////////////////
    def start_loop(self,tipo):

        start=1

        while start != 0:

            self.status_pagina()

            if tipo == 'mensagem':
                self.executa_mensagem()

            else:
                self.executa_qrcod()
            if self.status_arquivo == True:
                f=open(self.dir_sessao[tipo],"wt")
                f.write(self.loop_text)
                f.close()

            print(self.loop_print)
            start=self.loop_start

            self.time.sleep(5)
        self.set_perfil()
        self.time.sleep(1)
        self.browser.quit()
        self.time.sleep(1)
    #////////////////////////////////////////////////////////////////////////////////////
    def executa_mensagem(self):
        if self.loop_text == '<_>true<_>':

            for msgs in self.mensagens:
                cont=0;
                #self.atributo_set('[data-testid="icon-search-morph"]','click')
                self.tag_set( self.tag('[data-testid="icon-search-morph"]'), 'click' )
                self.time.sleep(1)
                status_msg=False
                for msg in msgs:#colocar verificador se carregol busca mensagens
                    if cont == 0:
                        tel=msg

                        tag_fone=self.tag('[data-testid="chat-list-search"]')
                        if tag_fone != False:
                            print('procurando telefone ...')
                            self.tag_set(tag_fone,tel)
                            print('telefone procurado: '+tel)
                            self.time.sleep(3)
                            self.tag_set(tag_fone,'enter')
                            print('enter telefone ')
                            telefone=tel

                        #self.atributo_set('[data-testid="chat-list-search"]','enter',tel,5)
                        cont=1
                        self.time.sleep(1)
                    else:
                        tag_msg=self.tag('[data-testid="conversation-compose-box-input"]')
                        if tag_msg != False:
                            self.tag_set(tag_msg,msg)
                            print('escrevendo :\n - '+telefone+' : ' +msg)
                            self.time.sleep(1)
                            self.tag_set(tag_msg,'enter')
                            print('enviando...')
                        status_msg=True
                        self.time.sleep(1)

                if status_msg == False:
                    for msg_glo in self.mensagem:
                        tag_txt=self.tag('[data-testid="conversation-compose-box-input"]')
                        #print('tag :'+tag_txt)
                        if tag_txt != False:
                            self.tag_set(tag_txt,msg_glo)
                            print('escrevendo :\n - '+telefone+' : ' +msg_glo)
                            self.time.sleep(2);
                            self.tag_set(tag_txt,'enter')
                            print('enviando...')

                        self.time.sleep(1)

            self.tag_set( self.tag('[data-testid="icon-search-morph"]'), 'click' )
            #print('click pesquizar fone')
            #    self.time.sleep(3)
            self.time.sleep(1)

    #-----------------------------------------------------
    def envia_msg(self):

        self.status={
            '0_0':
                {
                    'print':'carregando javascript...',
                    'text':'<_>loading<_>',
                    'loop':1
                },

            '0_1':
                {
                    'print':'você precisa ativar whatsapp web!',
                    'text':'<_>offline<_>',
                    'loop':0
                },

            '1_0':
                {
                    'print':'Mensagem enviada!',
                    'text':'<_>true<_>',
                    'loop':0
                },

            '1_1':
                {
                    'print':'Falha no sistema!',
                    'text':'<_>false<_>',
                    'loop':0
                }
        }

        self.start_loop('mensagem')
    #////////////////////////////////////////////////////////////////////////////////////
    def executa_qrcod(self):
        if self.loop_text == '<_>loop<_>': #condiconal envia mensagem
            status=self.atributo_get('[data-testid="qrcode"]','class')
            qrcod=self.atributo_get('[data-testid="qrcode"]','data-ref')

            if status == '_19vUU':

                self.loop_print='enviando qrcod :'+qrcod
                self.loop_text=qrcod
                self.loop_start=1

            elif status == '_1EP1P _19vUU':

                self.loop_start=0
                self.loop_print='parado...'
                self.loop_text='<_>parado<_>'
        elif self.loop_text == '<_>true<_>':
            print('pegando dados do login...')
            self.dados_login()
            #self.set_perfil()


    #-----------------------------------------------------
    def get_qrcod(self):
        self.status={
            '0_0':{
                'print':'carregando javascript...',
                'text':'<_>loading<_>',
                'loop':1
            },

            '0_1':{
                'text':'<_>loop<_>',
                'print':'',
                'loop':0
            },

            '1_0':{
                'print':'whatsapp web ativado!',
                'text':'<_>true<_>',
                'loop':0
            },

            '1_1':{
                'print':'Falha no sistema!',
                'text':'<_>false<_>',
                'loop':0
            }


        }

        self.start_loop('qrcod')
