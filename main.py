import json # Arquivos externos do codigo principal
import networkx as nx #Biblioteca para manipulação e criação de grafos
import matplotlib.pyplot as plt #Biblioteca para viazualizar grafos

# Clases

class Vertice: # Representa um vértice (nó) no grafo
    def __init__(self, rotulo):
        self.rotulo = rotulo
        self.adjacentes = []

    def adiciona_adjacente(self, adj):
        self.adjacentes.append(adj)


class Adjacente: # Representa um conexão(aresta) entre dois vertices
    def __init__(self, vertice, custo):
        self.vertice = vertice
        self.custo = custo


class Grafo: # Monta o grafo
    def __init__(self):
        with open("cidades.json", "r") as f: # Busca as cidades no arquivo Json
            dados = json.load(f)

        self.cidades = {nome: Vertice(nome) for nome in dados}

        for cidade, vizinhos in dados.items():
            for vizinho, custo in vizinhos.items():
                self.cidades[cidade].adiciona_adjacente(
                    Adjacente(self.cidades[vizinho], custo)
                )


# Heuristica

with open("heuristicas.json", "r") as f: # Busca a heuristica no arquivo Json
    heuristicas = json.load(f)


# Ida*

class IDAEstrela:
    def __init__(self, objetivo, grafo):
        self.objetivo = objetivo
        self.grafo = grafo

    def buscar(self, inicio):
        limite = heuristicas.get(self.objetivo.rotulo, {}).get(inicio.rotulo, 0)

        while True:
            resultado = self._busca(inicio, 0, limite, [inicio.rotulo])

            if isinstance(resultado, tuple):
                return resultado

            if resultado == float('inf'):
                return None

            limite = resultado

    def _busca(self, atual, g, limite, caminho):
        h = heuristicas.get(self.objetivo.rotulo, {}).get(atual.rotulo, 0)
        f = g + h

        if f > limite:
            return f

        if atual.rotulo == self.objetivo.rotulo:
            return caminho, self.custo_total(caminho)

        minimo = float('inf')

        for adj in atual.adjacentes:
            if adj.vertice.rotulo not in caminho:
                resultado = self._busca(
                    adj.vertice,
                    g + adj.custo,
                    limite,
                    caminho + [adj.vertice.rotulo]
                )

                if isinstance(resultado, tuple):
                    return resultado

                if resultado < minimo:
                    minimo = resultado

        return minimo

    def custo_total(self, caminho): # Dá o custo total do caminho
        custo = 0

        for i in range(len(caminho) - 1):
            atual = caminho[i]
            proximo = caminho[i + 1]

            for adj in self.grafo.cidades[atual].adjacentes:
                if adj.vertice.rotulo == proximo:
                    custo += adj.custo
                    break

        return custo


# Desenha o mapa

def desenhar_mapa(grafo, caminho=None): # Converte o grafo em uma vizuliação gráfica
    G = nx.Graph()

    for cidade in grafo.cidades.values():
        G.add_node(cidade.rotulo)

    for cidade in grafo.cidades.values():
        for adj in cidade.adjacentes:
            G.add_edge(cidade.rotulo, adj.vertice.rotulo, weight=adj.custo)
            
    # Posições baseadas no mapa real da Romênia
    pos = {
        "Oradea":    (0.35, 0.90),
        "Zerind":    (0.28, 0.80),
        "Arad":      (0.18, 0.68),
        "Timisoara": (0.15, 0.52),
        "Lugoj":     (0.28, 0.44),
        "Mehadia":   (0.32, 0.36),
        "Dobreta":   (0.25, 0.26),
        "Craiova":   (0.40, 0.20),
        "Rimnicu":   (0.48, 0.50),
        "Sibiu":     (0.50, 0.63),
        "Fagaras":   (0.63, 0.63),
        "Pitesti":   (0.58, 0.40),
        "Bucharest": (0.72, 0.28),
        "Giurgiu":   (0.68, 0.14),
        "Urziceni":  (0.85, 0.32),
        "Hirsova":   (0.95, 0.32),
        "Eforie":    (0.98, 0.18),
        "Vaslui":    (0.95, 0.55),
        "Iasi":      (0.90, 0.68),
        "Neamt":     (0.78, 0.78),
        }

    nx.draw(G, pos, with_labels=True, node_size=2000, font_size=8)

    if caminho:
        edges = list(zip(caminho, caminho[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=3)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.show()

# Main

if __name__ == "__main__": # Função de pedir os dados para a comparação do grafo
    print("=== IDA* - MAPA DE CIDADES ===")

    mapa = Grafo()

    origem = input("Digite a cidade de origem: ").strip()
    destino = input("Digite a cidade de destino: ").strip()

    if origem not in mapa.cidades or destino not in mapa.cidades:
        print("Cidade inválida!")
    else:
        ida = IDAEstrela(mapa.cidades[destino], mapa)
        resultado = ida.buscar(mapa.cidades[origem])

        if resultado:
            caminho, custo = resultado
            print("Caminho:", " -> ".join(caminho))
            print("Custo total:", custo)

            desenhar_mapa(mapa, caminho)
        else:
            print("Sem caminho encontrado.")
