<h1>Sistema de automação para seu WhatsApp </h1>
<h2>O que é?</h2>
<ul>
  <li>
    <p>Basicamente é uma class em Python que utiliza o selenium para sistemas de automação em navegadores que é responsável por fazer disparos de mensagens no seu Whatsapp</p>
  </li>
  <li>
    <p>A ideia é utilizar este projeto em conjunto com sistemas distintos como o PHP que poderá transmitir parâmetros através do padrão XML</p>
  </li>
</ul>
<h2>Como utilizar</h2>
<ul>
  <li>
    <p>O arquivo init.py tem um exemplo da funcionalidade da aplicação</p>
  </li>
  <li>
    <p>Basicamente você cria uma lista em XML com as especificações de execução da class, depois você pode executar a class através do shell</p>
  </li>
  <li>
    <p>ao executar a class sera feita uma varredura na pasta (input)</p>
  </li>
  <li>
    <p>Na pasta (input) você coloca as instruções de execução através de XML</p>
  </li>
  <li>
    <p>Na pasta (input) tem um arquivo XML com exemplo especifico dos parâmetros de execução.</p>
  </li>
</ul>

<h2>Tags de parâmetros XML</h2>
<ul>

  <li>
    <p>perfil</p>
    <ul>
      <li>user: para usuário do navegador</li>
      <li>sessao: para sessão do navegador</li>
    </ul>
  </li>

  <li>
    <p>exe: para os comandos (login, logoff, status)</p>
  </li>

  <li>
    <p>msg</p>
    <ul>
      <li>tel: telefone a receber mensagem</li>
      <li>txt: texto da mensagem</li>
    </ul>
  </li>
  <li>
    <p>somente as tags exe, tel, txt e msg podem receber vários parâmetros</p>
  </li>
</ul>
