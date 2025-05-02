from .models import Person, FamilyRelation
from collections import deque, defaultdict
import heapq


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

def dfs(graph, start_id, goal_id, visited=None):
    """
    Algorithme de parcours en profondeur (DFS)
    """
    if visited is None:
        visited = set()

    # Marquer le noeud comme visité
    visited.add(start_id)

    # Si nous avons trouvé le but, retourner la solution
    if start_id == goal_id:
        return [start_id]

    # Explore les voisins
    for neighbor, _ in graph[start_id]:
        if neighbor not in visited:
            path = dfs(graph, neighbor, goal_id, visited)
            if path:
                return [start_id] + path
    return None


def bfs(graph, start_id, goal_id):
    """
    Algorithme de parcours en largeur (BFS)
    """
    visited = set()
    queue = deque([(start_id, [start_id])])  # La queue contient les noeuds à visiter et le chemin

    while queue:
        current_node, path = queue.popleft()

        if current_node == goal_id:
            return path

        visited.add(current_node)

        for neighbor, _ in graph[current_node]:
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                visited.add(neighbor)

    return None


def dijkstra(graph, start_id, goal_id):
    """
    Algorithme de Dijkstra pour plus court chemin
    """
    # Initialisation des distances et du chemin
    distances = {node: float('inf') for node in graph}
    distances[start_id] = 0
    previous_nodes = {node: None for node in graph}
    priority_queue = [(0, start_id)]  # (distance, node)

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # Si le nœud actuel est le but, reconstruire le chemin
        if current_node == goal_id:
            path = []
            while previous_nodes[current_node] is not None:
                path.insert(0, current_node)
                current_node = previous_nodes[current_node]
            path.insert(0, start_id)
            return path

        # Si un nœud a déjà été visité avec une distance plus courte, ignorer
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return None


def bellman_ford(graph, start_id, goal_id):
    """
    Algorithme de Bellman-Ford pour plus court chemin avec poids négatifs
    """
    distances = {node: float('inf') for node in graph}
    distances[start_id] = 0
    previous_nodes = {node: None for node in graph}

    # Relaxer les arêtes (n-1) fois
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node]:
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
                    previous_nodes[neighbor] = node

    # Vérification de la présence de cycles négatifs
    for node in graph:
        for neighbor, weight in graph[node]:
            if distances[node] + weight < distances[neighbor]:
                raise ValueError("Graph contains a negative-weight cycle")

    # Reconstruire le chemin
    path = []
    current_node = goal_id
    while current_node is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]

    return path if distances[goal_id] < float('inf') else None


def prim(graph):
    """
    Algorithme de Prim pour arbre couvrant minimum (MST)
    """
    visited = set()
    edges = []
    start_node = next(iter(graph))  # Prendre n'importe quel nœud comme départ
    visited.add(start_node)

    # Utilisation d'un tas pour explorer les arêtes les moins coûteuses
    priority_queue = []
    for neighbor, weight in graph[start_node]:
        heapq.heappush(priority_queue, (weight, start_node, neighbor))

    while priority_queue:
        weight, from_node, to_node = heapq.heappop(priority_queue)

        if to_node not in visited:
            visited.add(to_node)
            edges.append((from_node, to_node, weight))

            for neighbor, weight in graph[to_node]:
                if neighbor not in visited:
                    heapq.heappush(priority_queue, (weight, to_node, neighbor))

    return edges


def kruskal(graph):
    """
    Algorithme de Kruskal pour arbre couvrant minimum (MST)
    """
    parent = {}
    rank = {}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)

        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    # Initialisation des parents et des rangs
    for node in graph:
        parent[node] = node
        rank[node] = 0

    edges = []
    for node in graph:
        for neighbor, weight in graph[node]:
            edges.append((weight, node, neighbor))

    edges.sort()

    mst = []

    for weight, node1, node2 in edges:
        if find(node1) != find(node2):
            union(node1, node2)
            mst.append((node1, node2, weight))

    return mst
