
#Importação da biblioteca
import matplotlib.pyplot as plt

#Variáveis globais
tamanhoDoDisco = 200
posicaoCabecaLeituraEscrita = 25
listaDePedidosOriginal = []
tamanhoListaPedidos = len(listaDePedidosOriginal)
medias = {}

#Rotinas
def lePedidosArquivo(nomeArquivo):
    with open(nomeArquivo) as arquivo:
        for linha in arquivo:
            listaDePedidosOriginal.append(int(linha.strip()))

    #Variável que armazena o tamanho da lista de pedidos
    global tamanhoListaPedidos
    tamanhoListaPedidos = len(listaDePedidosOriginal)



#Algoritmo FCFS: Solicitações de acesso ao disco são realizadas na ordem em que os pedidos são feitos.
def algoritmoFCFS(listaDePedidos):
    total = 0
    novaPosicaoCabecaLeituraEscrita = posicaoCabecaLeituraEscrita
    for i in range(tamanhoListaPedidos):
        total += abs(novaPosicaoCabecaLeituraEscrita - listaDePedidos[i])
        novaPosicaoCabecaLeituraEscrita = listaDePedidos[i]

    media = total / tamanhoListaPedidos
    return media

#Algoritmo SSTF: Pedidos são ordenados em relação a posição atual da cabeça de leitura/escrita.
def algoritmoSSTF(listaDePedidos):
    total = 0
    novaPosicaoCabecaLeituraEscrita = posicaoCabecaLeituraEscrita

    while len(listaDePedidos) > 0:
        valorMinimo = float("inf")
        index = None

        for i in listaDePedidos:
            diferencaDeValor = abs(novaPosicaoCabecaLeituraEscrita - i)
            if diferencaDeValor < valorMinimo:
                valorMinimo = diferencaDeValor
                index = listaDePedidos.index(i)

        total += valorMinimo
        novaPosicaoCabecaLeituraEscrita = listaDePedidos[index]
        listaDePedidos.pop(index)

    media = total / tamanhoListaPedidos
    return media

# Algoritmo SCAN: busca atender aos pedidos mais proximos da cabeça de leitura/escrita como o SSTF e busca atender pedidos primeiro em um sentido, depois troca.
def algoritmoSCAN(listaDePedidos):
    deslocamento = 0

    listaDePedidosOrdemDesc = sorted(listaDePedidos, reverse=True)

    if 0 not in listaDePedidosOrdemDesc:
        listaDePedidosOrdemDesc.append(0)

    index = listaDePedidosOrdemDesc.index(posicaoCabecaLeituraEscrita)

    posicaoAtual = posicaoCabecaLeituraEscrita

    deslocamentoFinalSCAN = [posicaoAtual]


    for j in range(index +1, len(listaDePedidosOrdemDesc)):
        proximaPosicao = listaDePedidosOrdemDesc[j]
        deslocamentoFinalSCAN.append(proximaPosicao)
        deslocamento += abs(posicaoAtual - proximaPosicao)
        posicaoAtual = proximaPosicao

    for j in range(index -1, -1, -1):
        proximaPosicao = listaDePedidosOrdemDesc[j]
        deslocamentoFinalSCAN.append(proximaPosicao)
        deslocamento += abs(posicaoAtual - proximaPosicao)
        posicaoAtual = proximaPosicao

    print(f"Ordem de deslocamento realizado pelo SCAN: {deslocamentoFinalSCAN}")

    media = deslocamento / len(listaDePedidosOrdemDesc)
    return media



#Algoritmo C-SCAN: Visa atender os pedidos que estão mais próximos da cabeça de leitura/escrita.
#Os pedidos são atendidos em um único sentido, indo de uma extremidade a outra.
def algoritmoCSCAN(listaDePedidos):
    deslocamento = 0
    
    if 199 not in listaDePedidos:
        listaDePedidos.append(199)

    if 0 not in listaDePedidos:
        listaDePedidos.append(0)


    listaDePedidosOrdemDesc = sorted(listaDePedidos)


    index = listaDePedidosOrdemDesc.index(posicaoCabecaLeituraEscrita)

    posicaoAtual = posicaoCabecaLeituraEscrita

    deslocamentoFinalC_SCAN = [posicaoAtual]


    for j in range(index +1, len(listaDePedidosOrdemDesc)):
        proximaPosicao = listaDePedidosOrdemDesc[j]
        deslocamentoFinalC_SCAN.append(proximaPosicao)
        deslocamento += abs(posicaoAtual - proximaPosicao)
        posicaoAtual = proximaPosicao

    for j in range(0, index -1, 1):
        proximaPosicao = listaDePedidosOrdemDesc[j]
        deslocamentoFinalC_SCAN.append(proximaPosicao)
        deslocamento += abs(posicaoAtual - proximaPosicao)
        posicaoAtual = proximaPosicao

    print(f"Ordem de deslocamento realizado pelo CSCAN: {deslocamentoFinalC_SCAN}")

    media = deslocamento / len(listaDePedidosOrdemDesc)
    return media

#Formação dos gráficos
def gerarGrafico(medias):
    plt.bar(range(len(medias)), list(medias.values()), align="center")
    plt.xticks(range(len(medias)), list(medias.keys()))
    plt.show()

#Função main
def main():
    print("Simulador de Algoritmos de Escalonamento de Braço de Disco")
    lePedidosArquivo("listaDePedidos.txt")
    print(f"Lista de Pedidos em questão: {listaDePedidosOriginal}")

    FCFS = algoritmoFCFS(listaDePedidosOriginal.copy())
    SCAN = algoritmoSCAN(listaDePedidosOriginal.copy())
    C_SCAN = algoritmoCSCAN(listaDePedidosOriginal.copy())
    SSTF = algoritmoSSTF(listaDePedidosOriginal.copy())


    medias["FCFS"] = FCFS
    medias["SSTF"] = SSTF
    medias["SCAN"] = SCAN
    medias["C-SCAN"] = C_SCAN

    print(f"Resultado da média de deslocamento FCFS: {FCFS}")
    print(f"Resultado da média de deslocamento SSTF: {SSTF}")
    print(f"Resultado da média de deslocamento SCAN: {SCAN}")
    print(f"Resultado da média de deslocamento C-SCAN: {C_SCAN}")

    gerarGrafico(medias)

main()