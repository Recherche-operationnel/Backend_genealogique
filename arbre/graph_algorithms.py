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
    """
    pass  # À implémenter

def kruskal():
    """
    Algorithme de Kruskal pour arbre couvrant minimum (MST)
    """
    pass  # À implémenter
