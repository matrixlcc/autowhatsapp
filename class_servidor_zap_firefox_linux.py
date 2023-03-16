class servidor_zap:
    def __init__(self,id_user='1',id_sessao='1',backend=True,driver=False,executa='login',diretorio_xml='input'):
        import os #para diretorios
        from datetime import datetime

        from selenium import webdriver #para automacao

        from selenium.webdriver.common.keys import Keys #para interação tag
        from selenium.webdriver.common.by import By #para seletores "identificar"
        from selenium.webdriver.common.action_chains import ActionChains  #alternativa ao send_keys
        import time

        from selenium.webdriver.firefox.options import Options #opções firefox


        self.datetime=datetime
        self.os=os

        self.webdriver=webdriver

        self.By=By
        self.Keys=Keys
        self.ActionChains=ActionChains
        self.time=time


        self.Options=Options


        self.diretorio_xml=diretorio_xml
        self.id_user=id_user
        self.id_sessao=id_sessao
        self.executa=executa
        self.driver=driver
        self.backend=backend

        self.qrcod=False
        self.imgqrcod=False
        self.msg_tel=[]
        self.msg_txt=[]

        self.operacao=False

        self.arquivo_analise=False
        self.arquivo_analise_conteudo=False
        self.fila_exe=[]


        self.operacoes_inicia()
    #////////////////////////////////////////////////////////////////////////////
    def operacoes_inicia(self):
        diretorio=self.diretorio_xml
        inicia_opr=True
        files = self.os.listdir(diretorio)
        for f in files:
            self.verifica_input_perfil(diretorio+'/'+f)
            self.verifica_input_exe()
            self.verifica_input_msg()
            print(self.fila_exe)

            if inicia_opr==True:
                inicia_opr=False
                self.id_user=self.id_user_proximo
                self.id_sessao=self.id_sessao_proximo
                self.firefox_opcoes()

            elif self.id_user != self.id_user_proximo and self.id_sessao != self.id_sessao_proximo:
                self.browser.quit()
                self.id_user=self.id_user_proximo
                self.id_sessao=self.id_sessao_proximo
                self.firefox_opcoes()

            self.operacoes_executa()

        for f in files:
            print('removendo :'+f)
            self.os.system("rm -r  "+diretorio+'/'+f)

        self.browser.quit()

    #////////////////////////////////////////////////////////////////////////////
    def operacoes_executa(self):

        if len(self.fila_exe) > 0:
            for opr in self.fila_exe:

                if opr == 'login':
                    self.relatorio_exe('inicia:login')
                    self.loop_qrcod_inicia()
                    self.relatorio_exe('termina:login')
                elif opr == 'msg':
                    self.relatorio_exe('inicia:msg')
                    self.loop_mensagem_inicia()
                    self.relatorio_exe('termina:msg')
                elif opr == 'logoff':
                    self.relatorio_exe('inicia:logoff')
                    self.loop_logoff_inicia()
                    self.relatorio_exe('itermina:logoff')
                elif opr == 'status':
                    self.relatorio_exe('inicia:status')
                    self.loop_status_inicia()
                    self.relatorio_exe('termina:status')


    #/////////////////////////////////////////////////////////////////////////////
    def verifica_input_perfil(self,dir='input/mensagens.xml'):
        xml=''
        with open(dir, 'r') as linha:
            xml=xml+linha.read()

        self.arquivo_analise=dir
        self.arquivo_analise_conteudo=xml

        per = xml
        per = per.replace("</perfil>", "<perfil>")
        per = per.replace("</user>", "<user>")
        per = per.replace("</sessao>", "<sessao>")

        per = per.split('<perfil>')

        id_user = per[1].split('<user>')
        self.id_user_proximo = id_user[1]
        id_sessao = per[1].split('<sessao>')
        self.id_sessao_proximo=id_sessao[1]
        print('id_user'+id_user[1])
        print('id_sessao'+id_sessao[1])
    #/////////////////////////////////////////////////////////////////////////////
    def verifica_input_exe(self):
        self.fila_exe.clear()
        exe=self.arquivo_analise_conteudo

        exe = exe.replace("</exe>", "<-><exe>")
        exe = exe.split('<exe>')

        for ex in exe:

            if (
                '<->' in ex
            ):
                self.fila_exe.append( ex.replace("<->", "") )


    #/////////////////////////////////////////////////////////////////////////////
    def verifica_input_msg(self):
        self.msg_tel.clear()
        self.msg_txt.clear()

        xml=self.arquivo_analise_conteudo


        campo_exe=False
        msg = xml
        msg = msg.replace("</msg>", "")
        msg = msg.replace("</tel>", "<-><tel>")
        msg = msg.replace("</txt>", "<-><txt>")
        msg = msg.split('<msg>')
        for lista in msg:

            msg_tel=[]
            msg_txt=[]

            armazena_tel=False
            armazena_txt=False

            telefone = lista.split('<tel>')
            for tel in telefone:
                if (
                    '<txt>' not in tel
                    and '<msg>' not in tel
                    and '<?xml' not in tel
                    and '<->' in tel
                ):
                    msg_tel.append(tel.replace("<->", ""))
                    armazena_tel=True

            texto = lista.split('<txt>')
            for txt in texto:
                if (
                    '<tel>' not in txt
                    and '<msg>' not in txt
                    and '<?xml' not in txt
                    and '<->' in txt
                ):
                    msg_txt.append(txt.replace("<->", ""))
                    armazena_txt=True

            if armazena_tel == True:
                self.msg_tel.append(msg_tel)
                if campo_exe==False:
                    campo_exe=True
                    self.fila_exe.append("msg")

            if armazena_txt == True:
                self.msg_txt.append(msg_txt)

        print(self.msg_tel)
        print(self.msg_txt)




    #/////////////////////////////////////////////////////////////////////////////
    def firefox_opcoes(self):

        self.options = self.Options()



        self.dir_raiz = self.os.getcwd()
        dir_sessao=self.barramento_set([self.dir_raiz, 'sessao', 'id_user'+self.id_user, 'id_sessao'+self.id_sessao])
        if self.driver!=False:
            self.dir_driver=self.barramento_set([self.dir_raiz, 'driver', self.driver])
        else:
            self.dir_driver='firefox'

        self.dir_navegador=self.barramento_set([dir_sessao, 'firefox'])
        self.dir_input=self.barramento_set([dir_sessao, 'input'])

        self.dir_relatorio=self.barramento_set([dir_sessao, 'relatorio.xml'])
        self.dir_login=self.barramento_set([dir_sessao, 'dados_login.xml'])
        self.dir_temp=self.barramento_set([dir_sessao, 'relatorio_temp.xml'])



        if self.os.path.isdir(self.dir_navegador) == False :
            self.os.makedirs(self.dir_navegador)
        if self.os.path.isdir(self.dir_input) == False :
            self.os.makedirs(self.dir_input)



        self.processo=self.executa


        self.relatorio_exe("servidor:loading",True)


        self.relatorio_exe("diretorio_do_perfil:"+self.dir_navegador)

        self.options.headless = self.backend

        self.firefox_inicia()


    #-------------------------------------------------------------------
    def firefox_inicia(self):
        self.relatorio_exe('abre:pagina')
        sessao_firefox = self.webdriver.FirefoxProfile(self.dir_navegador)#rf""+
        if self.driver != False:
            self.browser = self.webdriver.Firefox( options=self.options,firefox_profile=sessao_firefox,executable_path=self.dir_driver)#service=dir_driver,
        else:
            self.browser = self.webdriver.Firefox( options=self.options,firefox_profile=sessao_firefox)
        self.browser.get("about:support")
        self.actions = self.ActionChains(self.browser)

        start =1
        while start !=0 :
            self.time.sleep(1)

            dir_temp= self.tag('[id="profile-dir-box"]')
            if dir_temp !=False:
                dir_temp=self.tag_get(dir_temp)
                if dir_temp != False:
                    #self.relatorio_exe(dir_temp)
                    start =0
        self.dir_temp_sessao=dir_temp
        self.relatorio_exe("diretorio_temp:"+dir_temp)

        self.time.sleep(1)

        self.tag_set(self.tag('[class="wide-container"]'),'control','t')
        self.browser.get("https://web.whatsapp.com")


    #/////////////////////////////////////////////////////////////////////////////
    def perfil_backup(self):
        files_perfil=self.os.listdir(self.dir_navegador)

        blacklist=[

            'bookmarkbackups',
            'thumbnails',
            'minidumps',

            'datareporting',
            'addonStartup.json.lz4',
            'safebrowsing',

            'cache2',
            'crashes',
            'sessionstore-backups',
            'startupCache',
            'security_state',


        ]
        if len(files_perfil) > 0:

            self.relatorio_exe('perfil:parcial')

            for f in files_perfil:

                if f not in blacklist:
                    self.os.system("cp -r "+self.dir_temp_sessao+'/'+f+' '+self.dir_navegador)
        elif len(files_perfil) == 0 :
            self.relatorio_exe('perfil:completo')
            files = self.os.listdir(self.dir_temp_sessao)
            for f in files:
                self.os.system("cp -r "+self.dir_temp_sessao+'/'+f+' '+self.dir_navegador)

    #/////////////////////////////////////////////////////////////////////////////
    def barramento_set(self,diretorio=['c:','pasta']):
        return  '/'.join(diretorio)
    #////////////////////////////////////////////////////////////////////////////
    def tag_existe(self,atributo,valor):
        re=self.browser.find_elements(self.By.CSS_SELECTOR, '['+atributo+'="'+valor+'"]')
        if len(re) > 0:
            return '1'
        else:
            return '0'
    #/////////////////////////////////////////////////////////////////////////////

    def tag(self,nome_seletor,saida=0):
        re=self.browser.find_elements(self.By.CSS_SELECTOR, nome_seletor)
        if len(re) > 0:
            return re[saida]
        else:
            return False
    #/////////////////////////////////////////////////////////////////////////////
    def tag_set(self,tag,tipo="text",texto=""):
        if tag !=False:

            if tipo == 'click':

                self.actions.move_to_element(tag).click().perform()
                return True
            elif tipo == 'text':

                self.actions.move_to_element(tag).send_keys(texto).perform()
                return True
            elif tipo == 'enter':
                self.actions.move_to_element(tag).send_keys(self.Keys.ENTER).perform()
                return True
            elif tipo == 'control':

                self.actions.move_to_element(tag).send_keys(self.Keys.CONTROL + texto).perform()
                return True
            else:
                self.actions.move_to_element(tag).send_keys(tipo).perform()
                return True
        else:
            return False
    #/////////////////////////////////////////////////////////////////////////////
    def tag_get(self,tag,atributo=False):
        if tag !=False:
            if atributo == False:
                return tag.text
            else:
                return tag.get_attribute(atributo)
        else:
            return False

    #///////////////////////////////////////////////////////////////////////////////


    #////////////////////////////////////////////////////////////////////////////////
    def loop_global_status(self):

        loop_0=1
        carregamento=False

        while loop_0!=0:
            if self.tag('[data-testid="qrcode"]')!= False:
                return False

            elif self.tag('[data-testid="chatlist-header"]') != False:
                return True

            elif carregamento == False:
                carregamento=True

                self.relatorio_exe('javascript:loading',True)



    #////////////////////////////////////////////////////////////////////////////////
    def loop_logoff_inicia(self):
        login=self.loop_global_status()

        self.loop_logoff_executa(login)

        self.relatorio_exe('login:false',True)

    #-------------------------------------------------------
    def loop_logoff_executa(self,staus_qrcod):


        if self.os.path.isdir(self.dir_navegador) != False :
            self.relatorio_exe('perfil:deletado')
            self.os.system("rm -r  "+self.dir_navegador)


        if staus_qrcod == True:
            loop_logoff=1
            while loop_logoff!=0:


                bnt_menu=self.tag('[data-testid="menu-bar-menu"]')
                if self.tag('[data-testid="menu"]') != False and bnt_menu!=False:
                    self.tag_set(bnt_menu,'click')
                    class_menu=self.tag_get(bnt_menu,'class')
                    self.time.sleep(1)

                    loop_0=1
                    while loop_0!=False:
                        class_menu=self.tag_get(bnt_menu,'class')
                        if class_menu == '_3OtEr _2Qn52':

                            loop_1=1
                            while loop_1!=0:
                                menu_sair=self.tag('li[data-testid="mi-logout menu-item"] div[class="iWqod _1MZM5"]')
                                if menu_sair!=False:
                                    self.tag_set(menu_sair,'click')
                                    self.time.sleep(1)

                                    loop_2=1
                                    while loop_2!=0:
                                        bnt_conf_sair=self.tag('[data-testid="popup-controls-ok"]')
                                        txt_conf_sair=self.tag('div[data-testid="popup-controls-ok"] div[class="tvf2evcx m0h2a7mj lb5m6g5c j7l1k36l ktfrpxia nu7pwgvd gjuq5ydh"]')
                                        if bnt_conf_sair != False and txt_conf_sair!=False:
                                            self.tag_set(bnt_conf_sair,'click')
                                            self.time.sleep(1)

                                            loop_3=1
                                            while loop_3!=0:
                                                qrcod=self.tag('[data-testid="qrcode"]')
                                                if qrcod !=False:
                                                    loop_0=0
                                                    loop_1=0
                                                    loop_2=0
                                                    loop_3=0
                                                    loop_logoff=0


    #////////////////////////////////////////////////////////////////////////////////
    #-----------------------------------------------------
    def loop_qrcod_inicia(self):

        login=self.loop_global_status()

        if login == False:
            self.loop_qrcod_executa()

        elif login == True:

            self.perfil_backup()
            self.relatorio_exe('login:true',True)

        self.relatorio_exe('fim:true')



    #-------------------------------------------------------
    def loop_qrcod_executa(self):
        loop_0=1
        msg_logando=False
        while loop_0!=0:
            tag_qrcod=False
            qrcod_parado=False
            qrcod=False

            tag_loading=self.tag('[data-testid="wa-web-loading-screen"]')
            if tag_loading==False:
                tag_qrcod=self.tag('[data-testid="qrcode"]')
                qrcod_parado=self.tag_get(tag_qrcod,'class')
                qrcod=self.tag_get(tag_qrcod,'data-ref')
            elif msg_logando==False and tag_loading!=False:
                self.relatorio_exe('login:loading',True)
                msg_logando=True




            if qrcod!=False and self.imgqrcod!=qrcod:
                self.relatorio_exe('qrcod:'+qrcod,True)
                print(qrcod)
                self.imgqrcod=qrcod




            elif self.tag('[class="_3g4Pn _2HcPg"]')!=False:
                self.loop_qrcod_login()

                self.perfil_backup()
                self.relatorio_exe('login:true',True)

                loop_0=0

            elif qrcod_parado=='_1EP1P _19vUU':
                self.relatorio_exe('login:false',True)

                loop_0=0
            self.time.sleep(3)

    #-----------------------------------------------
    def loop_qrcod_login(self):
        loop_login=1
        while loop_login!=0:

            if self.tag_set(self.tag('[class="_3g4Pn _2HcPg"]'),'click' ) != False:

                foto=self.tag_get(self.tag('[style="height: 100%; width: 100%; visibility: visible;"]'),'src')
                nome=self.tag_get(self.tag('[data-testid="col-main-profile-input"]'))
                if foto != False and nome !=False:
                    data_atual = self.datetime.today()
                    texto='<?xml version="1.0"?><data>'+str(data_atual)+'</data><foto>'+foto+'</foto><nome>'+nome+'</nome>'
                    self.status_set(self.dir_login,texto)
                    self.relatorio_exe('usuario:'+nome)
                    loop_login=0
                    self.time.sleep(3)
                    self.tag_set(self.tag('[data-testid="btn-closer-drawer"]'),'click')#fecha dados usuario

    #/////////////////////////////////////////////////////////////////////
    def loop_status_inicia(self):

        login=self.loop_global_status()

        if login == False:
            self.relatorio_exe('login:false',True)


        elif login == True:
            self.relatorio_exe('login:true',True)


        self.relatorio_exe('sessão terminada!')

    #/////////////////////////////////////////////////////////////////////
    def loop_mensagem_inicia(self):

        login=self.loop_global_status()

        if login == False:
            self.relatorio_exe('login:false',True)

        elif login == True:
            self.loop_mensagem_executa()
            self.relatorio_exe('msg:true',True)
            self.time.sleep(5)#time da mensagem enviar
        self.relatorio_exe('fim:true')

    #-------------------------------------------------


    #--------------------------------------------------
    def loop_mensagem_escreve(self,msg):
        loop_msg=1

        while loop_msg!=0:
            print('loop escreve')
            if self.chat_tag == False:
                self.chat_titulo=self.tag_get(self.tag('[data-testid="conversation-info-header-chat-title"]'))
                self.chat_tag=self.tag('[data-testid="conversation-compose-box-input"]')

            if self.chat_tag != False:
                carregado=True
                loop_msg=0
                self.tag_set(self.chat_tag,msg)
                self.relatorio_exe('msg:'+self.chat_titulo+'<:/>'+msg)

                self.tag_set(self.chat_tag,'enter')
                print('enviando...')

    #--------------------------------------------------------
    def loop_mensagem_limpa(self):
        self.chat_titulo=False
        self.chat_tag=False
    #--------------------------------------------------------

    def loop_mensagem_telefone(self,tel):
        nome_tag_chat='[data-testid="chat"]'
        nome_tag_input='[data-testid="chat-list-search"]'
        nome_tag_lista_1='div[data-testid="contact-list-key"] div div div[data-testid="list-item-1"]'
        nome_tag_lista_off='[data-testid="search-no-results-without-keyword"]'
        nome_tag_bnt_close='[data-testid="btn-closer-drawer"]'#class="_2-1k7" #data-testid="btn-closer-drawer"

        nome_tag_input_selec='[data-testid="input-placeholder"]'

        loop_telefone=1
        while loop_telefone!=0:

            tag_chat=self.tag(nome_tag_chat)
            if tag_chat != False:
                self.tag_set(tag_chat,'click')
                self.time.sleep(1)

                loop_0=1
                while loop_0!=0:
                    tag_input=self.tag(nome_tag_input)
                    if tag_input!=False:
                        self.tag_set(tag_input,tel)
                        self.time.sleep(1)

                        loop_1=1
                        while loop_1!=0:
                            if self.tag(nome_tag_lista_1) != False:
                                exe_lista_1=self.tag_set(tag_input,'enter')
                                self.telefone=True
                                loop_telefone=0
                                loop_0=0
                                loop_1=0
                                print('telefone existe')
                                self.time.sleep(5)

                            elif self.tag(nome_tag_lista_off) != False:
                                tag_bnt_close=self.tag(nome_tag_bnt_close)
                                self.tag_set(tag_bnt_close,'click')#fecha
                                self.telefone=False
                                loop_telefone=0
                                loop_0=0
                                loop_1=0
                                self.relatorio_exe('telefone_off:'+tel)



    #-//////////////////////////////////////////////////////

    def loop_mensagem_executa(self):


        cont=0
        if len(self.msg_tel) > 0:
            for telefone in self.msg_tel:

                for tel in telefone:

                    self.loop_mensagem_telefone(tel)
                    self.loop_mensagem_limpa()
                    if self.telefone == True:
                        for msg in self.msg_txt[cont]:

                            self.loop_mensagem_escreve(msg)
                cont=cont+1
        else:
            self.relatorio_exe('mensagens:false',True)

        self.perfil_backup()

    #-------------------------------------------------------

    def status_set(self,arquivo,txt,tipo="wt"):
        f=open(arquivo,tipo)
        f.write(txt)
        f.close()
    #-------------------------------------------------------
    def relatorio_exe(self,conteudo,edita_temp=False,tag='dados'):
        now = self.datetime.now()
        hora = str(now.hour)+':'+str(now.minute)+':'+str(now.second)
        tipo="a"
        texto=""
        data_atual = self.datetime.today()
        data_atual = str(data_atual)
        if self.operacao==False:
            tipo="wt"
            texto='<?xml version="1.0"?>\n'
            texto=texto+'<user>'+self.id_user+'</user>\n'
            texto=texto+'<sessao>'+self.id_sessao+'</sessao>\n'
            texto=texto+'<data>'+data_atual+'</data>'
            texto=texto+'<processo>'+self.processo+'</processo>\n'
            self.operacao=True
        texto=texto+'<'+tag+'>'+hora+'<:/:>'+conteudo+'</'+tag+'>\n'
        self.status_set(self.dir_relatorio,texto,tipo)
        print(conteudo)

        if edita_temp == True:
            self.relatorio_temp(data_atual,conteudo)

    #-------------------------------------------------------
    def relatorio_temp(self,horas,conteudo):

        texto='<?xml version="1.0"?>\n'
        texto=texto+'<user>'+self.id_user+'</user>\n'
        texto=texto+'<sessao>'+self.id_sessao+'</sessao>\n'
        texto=texto+'<data>'+horas+'</data>\n'
        texto=texto+'<processo>'+self.processo+'</processo>\n'
        texto=texto+'<dados>'+conteudo+'</dados>\n'
        self.status_set(self.dir_temp,texto)


    #-------------------------------------------------------
    def get_mensagens(self):
        text=self.tag('[class="_11JPr selectable-text copyable-text"]')
        for msg in text:
            print('#: '+self.tag_get(msg))
