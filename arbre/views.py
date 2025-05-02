# views.py
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Person, FamilyRelation
from .serializers import PersonSerializer, FamilyRelationSerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .graph_algorithms import prim

@parser_classes([MultiPartParser, JSONParser])
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    parser_classes = (MultiPartParser, FormParser)  # Important pour les uploads

class FamilyRelationViewSet(viewsets.ModelViewSet):
    queryset = FamilyRelation.objects.all()
    serializer_class = FamilyRelationSerializer

@require_http_methods(["GET"])
def prim_algorithm_view(request, start_node_id):
    print("acces à la vue prim_algorithm_view")
    try:
        start_id = int(start_node_id)
        
        # Exécuter l'algorithme de Prim
        nodes, edges, total_weight = prim(start_id)
        
        # Formater les arêtes pour le frontend
        formatted_edges = [
            {
                "source": u,
                "target": v,
                "weight": w
            }
            for u, v, w in edges
        ]
        
        # Retourner les résultats au format JSON
        return JsonResponse({
            "success": True,
            "nodes": list(nodes),
            "edges": formatted_edges,
            "totalWeight": total_weight
        })
    except ValueError:
        return JsonResponse({
            "success": False,
            "error": "L'ID du nœud de départ doit être un entier."
        }, status=400)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e),
        }, status=500)