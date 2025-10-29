import requests

# USADA PARA CRIAÇÃO E LOGIN DE CONTA
usuarios = []

# USADA PARA INSCRIÇÃO NO CAMPEONATO
usuariosNoCampeonato = []

# ========== FUNÇÕES GERAIS ============

# IMPRIME UM DIC ANINHADO DE FORMA ORGANIZADA
def printaDic(dic, num=0):
    for key in dic.keys():
        if type(dic[key]) is dict:
            print(key)
            printaDic(dic[key], num+1)
        else:
            print(f'{num * ' '}{key}: {dic[key]}')
    return

# FORÇA O USUÁRIO A ESCOLHAR UMA OPÇÃO VÁLIDA DENTRO DE UMA LISTA DE OPÇÕES
def forca_opcao(msg, listaOpcoes):
    msg += '\n' + ' --- '.join(listaOpcoes) + '\n-->'
    opcoes = input(msg)
    while opcoes not in listaOpcoes:
        opcoes = input(msg)
    return opcoes

# CRIA OS ÍNDICES DOS PRODUTOS E SEUS ITENS RELACIONADOS NA LOJA
def cria_indiceLoja():
    indicesLoja = {}
    for i in range(len(loja['Produtos'])):
        indicesLoja[loja['Produtos'][i]] = i
    return indicesLoja

# GARANTE QUE O VALOR DIGITADO SEJA UM NÚMERO
def verificaNum(msg):
    num = input(msg)
    while not num.isnumeric():
        num = input(msg)
    return int(num)


# ========== FUNÇÕES DO CLIENTE/USUÁRIO ==========

# PERMITE O USUÁRIO CRIAR UMA CONTA
def criar_conta():
    print("\n=== Criar Conta ===")
    nome = input('Nome completo: ')
    email = input('Email: ').lower()

    for usuario in usuarios:
        if usuario['email'] == email:
            print('Esse email já possui um cadastro!')
            return

    senha = input('Senha: ')
    confirmar = input('Confirme sua senha: ')
    if senha != confirmar:
        print('As senha não coincidem! ')
        return
    usuarios.append({'nome': nome, 'email': email, 'senha': senha})
    print('Conta criada com sucesso! ')

# REALIZA O LOGIN DA CONTA
def login():
    print("\n=== Login ===")
    email = input('Email: ').lower()
    senha = input('Senha: ')

    for usuario in usuarios:
        if usuario['email'] == email and usuario['senha'] == senha:
            print(f"Bem vindo {usuario['nome']}")
            return True
        print('Você não possui uma conta aqui!')
        return False

# CADASTRAR ENDEREÇO DO USUÁRIO
def cadastro_endereco():
    while True:
        # PELO CEP VAI BUSCAR O SEU ENDEREÇO USANDO O JSON
        cep = input('Diga seu cep: ')
        endereco = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if endereco.status_code == 200:
            carrinho['Endereço'] = endereco.json()
            carrinho['Endereço']['Nº'] = input('Numero da residencia: ')
            carrinho['Endereço']['Complemento'] = input('Complemento: ')
            break
        else:
            print('Cep invalido')
        return

# PERMITE O USUÁRIO COMPRAR UM ITEM DA LOJA
def comprar():
    item = forca_opcao('Qual produto vc deseja? \n-->', loja['Produtos'])
    indice_item = indicesLoja[item]
    for key in loja.keys():
        print(f'{key}: {loja[key][indice_item]}')
        if forca_opcao(f'Vc qr levar o/a {item}? \n-->', ['Sim', 'Não']) == 'Não':
            return

    qtd = verificaNum('Qnts unidade vc deseja? \n-->')
    if qtd <= loja['Estoque'][indice_item]:
        loja['Estoque'][indice_item] -= qtd
        carrinho['Valor Total'] += qtd * loja['Preço'][indice_item]

        if item not in carrinho.keys():
            carrinho['Itens'][item] = qtd
        else:
            carrinho['Itens'][item] += qtd
    else:
        print(f'Só há {loja['Estoque'][indice_item]} unidades no estoque')
    return

# EXIBE RESUMO DA COMPRA E PERMITE REMOÇAO DE ITENS ANTES DE FINALIZAR A COMPRA
def confirmarCompra():
    print('Essas são as informações da sua compra:')
    printaDic(carrinho)
    alterar = forca_opcao("Deseja remover algum item?", ['s', 'n'])
    if alterar == 's':
        item = forca_opcao("Qual item vc irá remover?", carrinho['Itens'].keys())
        indice = indicesLoja[item]
        qtd = verificaNum(f"Quantos kg de {item} serão removidos?")
        if qtd <= carrinho['Itens'][item]:
            carrinho['Itens'][item] -= qtd
            carrinho['Valor Total'] -= qtd * loja['Preço/kg'][indice]
        else:
            print(f"Não é possível remover esse tanto pois só há {carrinho['Itens'][item]}kg")
        confirmarCompra()
    return

# PERMITE A INSCRIÇÃO DE ALGUM DOS CAMPEONATOS DO PASSA À BOLA
def nosso_camp():
    nome = input('Nome completo: ')
    email = input('Email: ').lower()
    cpf = input('CPF:')
    while not cpf.isnumeric():
        cpf = input('CPF (somente números):')
    usuariosNoCampeonato.append({'nome': nome, 'email': email, 'cpf': cpf})
    print('Incrição realizada com sucesso!')
    return

# AÇÕES DO CLIENTE
acoesCliente = {
    'Campeonato': nosso_camp,
    'Entrar': login,
    'Criar Conta': criar_conta
}

# ============ FUNÇÕES DO ADMINISTRADOR NA LOJA ============

# FUNÇÃO QUE PERMITE ADICIONAR UM NOVO PRODUTO NA LOJA DO PASSA À BOLA
def adicionarItem_loja():
    global indicesLoja
    for key in loja.keys():
        if key in ['Preço', 'Estoque']:
            while True:
                try:
                    info = float(input(f'Diga o/a novo/a {key}: '))
                except:
                    print('Tem que ser float')
                else:
                    loja[key].append(info)
        info = float(input(f'Diga o/a novo/a {key}: '))
        loja[key].append(info)
    indicesLoja = cria_indiceLoja()
    return

# FUNÇÃO QUE PERMITE REMOVER UM PRODUTO NA LOJA DO PASSA À BOLA
def removerItem_loja():
    global indicesLoja
    escolha = forca_opcao('Qual produto vc deseja remover? \n-->', loja['Produtos'])
    indice_escolha = indicesLoja[escolha]
    for key in loja.keys():
        loja[key].pop(indice_escolha)
    indicesLoja = cria_indiceLoja()
    return

# FUNÇÃO QUE PERMITE ATUALIZAR UM PRODUTO NA LOJA DO PASSA À BOLA
def atualizarItem_loja():
    escolha = forca_opcao('Qual produto vc deseja atualizar: \n-->', loja['Produtos'])
    indice_escolha = indicesLoja[escolha]
    keys = list(loja.keys())
    keys.pop(0)
    for key in keys:
        if forca_opcao(f'Qr atualizar {key} para {escolha}? ', ['sim', 'não']) == 'sim':
            info = input(f'Diga o novo/a {key}: ')
            loja[key][indice_escolha] = info
    return

# =========== FUNÇÕES DO ADMINISTRADOR NOS TEXTOS ==========

# FUNÇÃO QUE PERMITE ADICIONAR UM NOVO TEXTO NAS NOTÍCIAS, JOGOS OU TRANSFERÊNCIAS
def adicionarItem_textos():
    global indicesTextos
    for key in conteudosTextos.keys():
        while True:
            info = input(f'Diga o/a novo/a {key} (ou aperte ENTER para pular): ')
            if info.strip() == '':
                break
            conteudosTextos[key].append('\n' + info)
            print(f'Textos adicionado com sucesso em {key}!')
    return

# FUNÇÃO QUE PERMITE REMOVER UM TEXTO NAS NOTÍCIAS, JOGOS OU TRANSFERÊNCIAS
def removerItem_textos():
    for key in conteudosTextos.keys():
        while True:
            print(f'\n--- {key} ---')
            for i, texto in enumerate(conteudosTextos[key], start=1):
                print(f'{i}. {texto.strip()}')

            escolha = input(f'\nDiga o nº do texto que você quer remover de {key} (ou aperte ENTER para pular): ')

            if escolha.strip() == '':
                break

            while not escolha.isnumeric():
                escolha = input('Digite um número válido: ')

            indice_escolha = int(escolha) - 1

            if 0 <= indice_escolha < len(conteudosTextos[key]):
                itemRemovido = conteudosTextos[key].pop(indice_escolha)
                print(f'\nRemovido com sucesso: {itemRemovido.strip()}')
            else:
                print('Número inválido.')
    return

# FUNÇÃO QUE PERMITE ATUALIZAR UM TEXTO NAS NOTÍCIAS, JOGOS OU TRANSFERÊNCIAS
def atualizarItem_textos():
    for key in conteudosTextos.keys():
        while True:
            print(f'\n--- {key} ---')
            for i, texto in enumerate(conteudosTextos[key], start=1):
                print(f'{i}. {texto.strip()}')

            escolha = input(f'\nDiga o nº do texto que você quer atualizar em {key} (ou aperte ENTER para pular): ')

            if escolha.strip() == '':
                break

            while not escolha.isnumeric():
                escolha = input('Digite um número válido: ')

            indice_escolha = int(escolha) - 1

            if 0 <= indice_escolha < len(conteudosTextos[key]):
                novo_texto = input(f'Digite o novo texto para substituir "{conteudosTextos[key][indice_escolha].strip()}":\n--> ')
                conteudosTextos[key][indice_escolha] = '\n' + novo_texto
                print(f'\nTexto atualizado com sucesso!')
            else:
                print('Número inválido.')
    return


# AÇÕES DO ADMINISTRADOR NA LOJA
acoesAdmin_loja = {
    'Adicionar': adicionarItem_loja,
    'Remover': removerItem_loja,
    'Atualizar': atualizarItem_loja
}

# AÇÕES DO ADMINISTRADOR NOS TEXTOS
acoesAdmin_textos ={
    'Adicionar': adicionarItem_textos,
    'Remover': removerItem_textos,
    'Atualizar': atualizarItem_textos

}

# ========== DIC REPRESENTANDO A LOJA DO PASSA À BOLA ==========
loja = {
    'Produtos': ['Camiseta Unissex', 'Caneca', 'Bola', 'Shorts', 'Moletom esportivo', 'Chaveiro'],
    'Preço': [89.90, 34.50, 129.90, 79.90, 189.90, 19.90],
    'Estoque': [120, 55, 88, 0, 155, 90]
}

# ========== DIC CARRINHO DA LOJA DO PASSA à BOLA ============
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

# ============ MENU COM AS OPÇÕES DO SITE ============
conteudosTextos = {
    'Notícias': ['\nGabi Zanotti marcou na final do Brasileirão Feminino.',
                 '\nMarta anuncia aposentadoria da Seleção Brasileira.'],

    'Jogos': ['\n21/08/2025 - Palmeiras 2x1 Corinthians (Allianz Parque)',
              '\n28/08/2025 - Corinthians 3x0 Ferroviária (Neo Química Arena)'],

    'Transferências': ['\nLizbeth Ovalle - Tiger → Orlando Pride (U$ 1,5 milhão)',
                       '\nAry Borges - Palmeiras → Chelsea (Gratuito)']
}

indicesLoja = cria_indiceLoja()

# ============ PÁGINA INICIAL DO SITE =============
def lin():
    print('---'*40)

lin()
print('Passa a Bola:     Home - Notícias - Jogos - Transferências - Nosso Campeonato - Loja - Entrar - Criar Conta\n')
print('O Futebol feminino na Palma da Sua Mão'.center(70))
print('Conectando tecnologia e paixão, Passa a Bola é o seu portal completo para o'
      '\nuniverso do futebol feminino. Notícias, jogos, transferências e muito mais.'.center(70))
lin()

print('----- BEM VINDO AO PASSA À BOLA -----')
pessoa = forca_opcao('Vc é cliente ou administrador? ', ['Cliente', 'Administrador'])
while True:
    if pessoa == 'Administrador':
        escolha = forca_opcao('Em qual você irá mexer?', ['Textos', 'Lojas'])
        if escolha == 'Textos':
            processo = forca_opcao('Oq vc deseja fazer nos textos?', acoesAdmin_textos.keys())
            acoesAdmin_textos[processo]()
        else:
            processo = forca_opcao('Oq vc deseja fazer na loja?', acoesAdmin_loja.keys())
            acoesAdmin_loja[processo]()

        cont = forca_opcao('Vc deseja continuar?', ['Sim', 'Não'])
        if cont == 'Não':
            print('\nTodas as mudanças foram salvas com sucesso! ')
            break
    else:
        escolha = forca_opcao('Oque você deseja ver?', ['Notícias', 'Jogos', 'Transferências', 'Loja' ,'Campeonatos', 'Entrar', 'Criar Conta'])
        if escolha in conteudosTextos:
            print(f'\n--- {escolha} ---')
            for item in conteudosTextos[escolha]:
                print(item)
        elif escolha in acoesCliente.keys():
            acoesCliente[escolha]()
        else:
            cadastro_endereco()
            comprar()
            confirmarCompra()

            if forca_opcao('Vc deseja continuar comprando? \n-->', ['Sim', 'Não']) == 'Não':
                itens = ', '.join(list(carrinho['Itens'].keys()))
                print(f'Vc vai levar {itens}, totalizando R${carrinho['Valor Total']} '
                      f'e será entregue na {carrinho['Endereço']['logradouro']}')
                print(carrinho)
                print('Obrigado pela compra! 😊')

        if forca_opcao('Você deseja ver ou fazer mais alguma coisa?', ['Sim', 'Não']) == 'Não':
            print('Obrigado pela visita! ⚽')
            break