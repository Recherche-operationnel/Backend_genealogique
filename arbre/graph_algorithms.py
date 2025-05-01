from .models import Person, FamilyRelation
from collections import deque, defaultdict

# Fonction utilitaire pour construire le graphe
def build_graph():
    graph = defaultdict(list)
    relations = FamilyRelation.objects.all()
    for rel in relations:
        from_id = rel.from_person.id
        to_id = rel.to_person.id

        # Ajout des liens en fonction du type de relation
        graph[from_id].append((to_id, 1))  # poids 1 par défaut
        if rel.type == 'spouse':
            graph[to_id].append((from_id, 1))  # relation bidirectionnelle
    return graph

# ---- ALGORITHMES DE GRAPHE ----

def dfs(start_id, goal_id):
    """
    Algorithme de parcours en profondeur (DFS)
    """
    pass  # À implémenter

def bfs(start_id, goal_id):
    """
    Algorithme de parcours en largeur (BFS)
    """
    pass  # À implémenter

def dijkstra(start_id, goal_id):
    """
    Algorithme de Dijkstra pour plus court chemin
    """
    pass  # À implémenter

def bellman_ford(start_id, goal_id):
    """
    Algorithme de Bellman-Ford pour plus court chemin avec poids négatifs
    """
    pass  # À implémenter

def prim(start_id=None):
    """
    Algorithme de Prim pour arbre couvrant minimum (MST)
    
    Entrée:
        graph: un dictionnaire où les clés sont les IDs des personnes et 
               les valeurs sont des listes de tuples (id_dest, poids)
    
    Sortie:
        Un tuple (arbre_sommets, arbre_aretes, poids_total) représentant l'arbre couvrant de poids minimum
    
    """
    graph = build_graph()
    relations = FamilyRelation.objects.all()
    print(graph)
    print(relations)
    #Initialisation du resultat
    nodes_in_mst = {start_id}
    mst_edges = []
    total_weight = 0

    graph_nodes = set(graph.keys())

    while nodes_in_mst != graph_nodes:
        #On cherche le plus petit poids de l'arbre
        min_edge = None
        for node in nodes_in_mst:
            #on cherche l'arete de poids minimum
            for neighbor, weight in graph[node]:
                if neighbor not in nodes_in_mst:
                    if min_edge is None or weight < min_edge[2]:
                        min_edge = (node, neighbor, weight)

        if min_edge is None:
            print("Le graphe n'est pas connexe")
        
        u,v, weight = min_edge
        mst_edges.append(min_edge)
        nodes_in_mst.add(v)
        total_weight += weight

        return mst_edges, nodes_in_mst, total_weight
    # #tant que  tout les noeuds de l'arbre ne sont pas explorés
    # while set(nodes_in_mst) != set(graph):
    #     #On cherche le plus petit poids de l'arbre
    #     min_edge = None
    #     for node in nodes_in_mst:
    #         for neighbor in graph:
    #             if neighbor not in nodes_in_mst:
    #                 if min_edge is None :
    #                     min_edge = (node, neighbor)

       
    pass  # À implémenter

def kruskal():
    """
    Algorithme de Kruskal pour arbre couvrant minimum (MST)
    """
    pass  # À implémenter
