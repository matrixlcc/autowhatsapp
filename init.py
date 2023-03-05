from class_servidor_zap_firefox_linux import servidor_zap

mensagens=[
    ['999999999','ola boot teste 1'],
    ['911111111'],
]
mensagem_para_todos=["bom dia","Teste boot"]

print("####################################")
print("########### AUTOWHATSAPP ###########")
print("####################################")
tarefa = input("Escolha:\n(l) para login \n(m) para mensagens :")
if tarefa == 'l' :
    zap=servidor_zap(
        id_user='1',
        id_sessao='1',
        status_arquivo=True,
        backend=False
    )
    zap.get_qrcod()
else:
    zap=servidor_zap(
        id_user='1',
        id_sessao='1',
        status_arquivo=True,
        backend=True
    )
    zap.mensagens=mensagens
    zap.mensagem=mensagem_para_todos
    zap.envia_msg()
