Relatório Técnico: Desenvolvimento e Implementação de um Cliente FTP em Python
1. Introdução ao protocolo FTP
O File Transfer Protocol (FTP), ou Protocolo de Transferência de Arquivos, é um dos protocolos de rede mais antigos e fundamentais da camada de aplicação do modelo TCP/IP. Sua finalidade principal é permitir a transferência de arquivos entre um cliente e um servidor. A arquitetura do FTP baseia-se em duas conexões distintas: uma porta de controle (geralmente a porta 21), por onde trafegam os comandos e respostas, e uma porta de dados (tradicionalmente a porta 20, ou portas altas dinâmicas em modo passivo), responsável pelo tráfego real dos arquivos.

Apesar de sua eficiência histórica, o FTP original transmite tanto os dados quanto as credenciais (usuário e senha) em texto plano, sem qualquer tipo de criptografia, o que exige cuidados na sua implementação em redes modernas.

2. Descrição da solução escolhida
Para atender aos requisitos propostos pela disciplina, foi desenvolvida uma aplicação cliente via Interface de Linha de Comando (CLI) utilizando a linguagem Python.

A escolha do Python justifica-se pela sua robusta biblioteca padrão para protocolos de rede. A solução utiliza a biblioteca nativa ftplib, que encapsula a complexidade dos sockets e lida diretamente com os comandos padronizados do servidor FTP. Para complementar a solução e melhorar a robustez, foram incorporadas as bibliotecas pathlib (para manipulação padronizada de caminhos de arquivos, independente do sistema operacional) e a biblioteca externa tqdm (para fornecer feedback visual ao usuário através de barras de progresso durante as transferências de dados).

3. Etapas realizadas
O projeto seguiu um ciclo prático de desenvolvimento e testes no ambiente PyCharm:

Modelagem Orientada a Objetos: Criação da classe ClienteFTPAvancado para centralizar a lógica de conexão (connect, login) e transferência.

Implementação de Funcionalidades Essenciais:

Utilização do comando LIST (retrlines) para exibir o diretório remoto.

Utilização de transferências binárias (RETR via retrbinary e STOR via storbinary) para garantir o download e upload íntegro de qualquer formato de arquivo.

Desenvolvimento da Interface Interativa: Criação de um menu de terminal via laço de repetição (while True), permitindo ao usuário escolher opções numéricas (1 a 4) de forma intuitiva.

Tratamento de Exceções (Try/Except): Mapeamento de possíveis falhas de rede e permissão, impedindo o encerramento abrupto (crash) do sistema.

Bateria de Testes Práticos: Execução do cliente contra o servidor público de testes test.rebex.net para validar o comportamento real do protocolo.

4. Resultados obtidos
A solução cumpriu integralmente os objetivos propostos. Durante a execução, o cliente foi capaz de conectar-se com sucesso ao servidor de testes.

A listagem do diretório remoto funcionou corretamente, permitindo visualizar os arquivos disponíveis.

Foi realizado com sucesso o download binário do arquivo readme.txt do servidor para o armazenamento local.

O sistema provou ser altamente resiliente através do tratamento de erros: ao simular uma tentativa de conexão com credenciais incorretas, o programa capturou perfeitamente o código de resposta do servidor (530 Authentication rejected) e encerrou com o código de saída 0 (exit code 0), indicando um encerramento seguro e controlado, em vez de uma falha de software.

5. Dificuldades encontradas
Durante a codificação e os testes práticos na IDE (PyCharm), foram encontradas e superadas algumas dificuldades técnicas e lógicas:

Erros de Sintaxe e Importação: Ocorreram alertas iniciais da IDE quanto à sintaxe de importação de módulos específicos (ex: correção para from pathlib import Path) e identificação de parênteses não fechados em definições de funções (ex: SyntaxError: '(' was never closed), que exigiram depuração e correção na estruturação do código.

Fluxo de Interação do Usuário (UX): Na etapa de testes do terminal, notou-se um desafio na sincronia das entradas (inputs). O sistema esperava primeiramente o número do comando (ex: 2 para baixar) para só depois solicitar a string com o nome do arquivo (readme.txt). Entradas sobrepostas geraram erros de "Opção Inválida", sendo rapidamente corrigidas ao alinhar o entendimento do fluxo em duas etapas do terminal.

Restrições de Servidor: Ao testar a funcionalidade de upload, o servidor público de testes recusou o arquivo devido a políticas de segurança de gravação, o que, embora tenha impedido o envio prático, serviu como excelente laboratório para atestar o funcionamento da captura de erros de permissão do nosso cliente FTP.

6. Conclusão crítica sobre o uso do FTP
A atividade prática consolidou o entendimento teórico de como as aplicações cliente-servidor se comunicam e negociam transferências de dados "por baixo dos panos". O FTP demonstrou ser um protocolo muito rápido e direto para envio de arquivos.

No entanto, com os testes, ficou evidente que a falta de segurança nativa do FTP o torna obsoleto para ambientes de produção que trafegam dados sensíveis ou operam na internet aberta. A vulnerabilidade de interceptação de dados (sniffing) exige que implementações reais utilizem camadas de segurança adicionais. Como aprendizado, a própria ferramenta desenvolvida já possui a arquitetura preparada para habilitar o FTPS (FTP over TLS/SSL) através da biblioteca FTP_TLS, o que mitigaria esses riscos garantindo confidencialidade na autenticação e integridade na transmissão.
