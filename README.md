# ⚽👧 Passa à Bola

O projeto “Passa à Bola” é uma aplicação em Python que simula o funcionamento de um site interativo sobre futebol feminino, combinando um portal de notícias e jogos com um sistema de e-commerce e cadastro de campeonatos.
Ele foi desenvolvido como um exercício prático de lógica de programação, utilizando funções, dicionários, loops, validações e integração com API externa (ViaCEP) para tornar o sistema mais dinâmico e realista.

---

## 🧩 Estrutura Geral

O código está dividido em blocos principais:

- Funções gerais → usadas por várias partes do programa (ex: validação, impressão, menus)
- Funções do cliente/usuário → criação de conta, login, compra, endereço, campeonato
- Funções do administrador (loja e textos) → adicionar/remover/atualizar produtos e notícias
- Dicionários principais → loja, carrinho, conteúdos de textos
- Menu inicial interativo → define o fluxo entre cliente e administrador

---

## ⚙️ Funções Gerais

- printaDic(dic, num=0): Imprime dicionários (inclusive aninhados) de forma organizada e indentada.
- forca_opcao(msg, listaOpcoes): Garante que o usuário escolha uma opção válida entre as listadas (impede erros).
- cria_indiceLoja(): Cria um índice que liga cada produto ao seu número dentro das listas da loja.
- verificaNum(msg): Só aceita números inteiros como entrada (validação de quantidades, por exemplo).

---

## 👤 Funções do Cliente/Usuário

🔐 Conta e Login

- criar_conta(): Permite o usuário cadastrar nome, e-mail e senha. Impede e-mails duplicados.
- login(): Confere e-mail e senha para permitir entrada no sistema.


🏠 Cadastro de Endereço

- cadastro_endereco(): o usuário informa o CEP, e o sistema consulta automaticamente o site ViaCEP (API pública) para preencher o endereço.
Depois, o usuário adiciona o número e complemento da casa.


🛒 Compra de Produtos

- comprar(): Mostra os produtos disponíveis, permite escolher e confirmar a compra. Atualiza o estoque e o valor total no carrinho.
Também soma a quantidade no dicionário de itens comprados.
- confirmarCompra(): Exibe o resumo da compra e dá a opção de remover itens antes de finalizar.


🏆 Campeonato

- nosso_camp(): Faz a inscrição de um usuário no campeonato, coletando nome, e-mail e CPF (validado como numérico).

---

## 🧮 Funções do Administrador

🏬 Administração da Loja

Permite o controle total do estoque de produtos:

- adicionarItem_loja(): Adiciona um novo produto na loja, pedindo nome, preço e estoque. Atualiza os índices.
- removerItem_loja(): Remove completamente um produto de todas as listas da loja.
- atualizarItem_loja(): Atualiza informações (preço, estoque, nome etc.) de um produto existente.


As ações estão agrupadas no dicionário:

acoesAdmin_loja = {

    'Adicionar': adicionarItem_loja,
    
    'Remover': removerItem_loja,
    
    'Atualizar': atualizarItem_loja
}


📰 Administração dos Textos (Notícias, Jogos e Transferências)

Permite gerenciar os conteúdos exibidos no site:

- adicionarItem_textos(): Adiciona novos textos em qualquer categoria (Notícias, Jogos ou Transferências).
- removerItem_textos(): Exibe todos os textos numerados e permite remover pelo número.
- atualizarItem_textos(): Substitui textos antigos por versões novas.


Essas ações estão no dicionário:

acoesAdmin_textos = {

    'Adicionar': adicionarItem_textos,
    
    'Remover': removerItem_textos,
    
    'Atualizar': atualizarItem_textos
}

---

## 🧾 Dicionários de Dados

🏪 Loja
loja = {

    'Produtos': ['Camiseta Unissex', 'Caneca', 'Bola', 'Shorts', 'Moletom esportivo', 'Chaveiro'],
    
    'Preço': [89.90, 34.50, 129.90, 79.90, 189.90, 19.90],
    
    'Estoque': [120, 55, 88, 0, 155, 90]
}

Armazena o catálogo de produtos com preços e estoque.


🛍️ Carrinho

carrinho = {

    'Endereço': {
    
        'Rua': '',
        
        'Bairro': '',
        
        'Nº': '',
        
        'CEP': ''
    },
    'Itens': {},
    
    'Valor Total': 0
}

Guarda os produtos comprados, o endereço do comprador e o valor total acumulado.


conteudosTextos = {

    'Notícias': [...],
    
    'Jogos': [...],
    
    'Transferências': [...]
}


Contém as notícias e informações exibidas na parte pública do site.

---

## 💻 Menu Principal (Interface do Usuário)

O sistema inicia com a “página inicial” do site:

print('Passa a Bola: Home - Notícias - Jogos - Transferências - Nosso Campeonato - Loja - Entrar - Criar Conta')

Depois pergunta:

pessoa = forca_opcao('Vc é cliente ou administrador?', ['Cliente', 'Administrador'])


Se for Administrador:

- Pode escolher entre Textos ou Loja
- Escolher se quer Adicionar, Remover ou Atualizar
- Repetir ou sair do painel


Se for Cliente:

- Pode ver Notícias, Jogos, Transferências
- Fazer Login, Criar Conta, Comprar na loja, ou inscrever-se no campeonato
- Se escolher loja, faz o fluxo completo: endereço → compra → confirmação → resumo da compra

---

## 🔚 Encerramento

O programa finaliza com uma mensagem amigável:

print('Obrigado pela visita! ⚽')

---

## 📚 Tecnologias Usadas

- Python 3
- Requests: utilizada para integração com a API ViaCEP, permitindo buscar automaticamente o endereço do usuário a partir do CEP digitado

---

## 🚀 Como Usar

1. Clone o projeto ou baixe o projeto
2. Instale as dependências: pip install requests 
3. Execute o script: python sprint04.py 
4. Escolha se é Cliente ou Administrador
5. Siga as opções exibidas no terminal

---

## 👨‍💻 Autor

Guilherme Barone Milani

Projeto desenvolvido como exercício prático de Python, com foco em:

- Estruturação de código por funções
- Manipulação de dicionários e listas
- Criação de menus interativos com loops
- Integração com API externa (ViaCEP)
- Simulação completa de um site e loja de futebol feminino
