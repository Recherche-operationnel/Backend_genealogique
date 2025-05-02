# views.py
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Person, FamilyRelation
from .serializers import PersonSerializer, FamilyRelationSerializer
from rest_framework.decorators import parser_classes
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, JSONParser
from django.http import JsonResponse
from .graph_algorithms import build_graph, dfs, bfs, dijkstra
from django.views.decorators.csrf import csrf_exempt
import json

@parser_classes([MultiPartParser, JSONParser])
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    parser_classes = (MultiPartParser, FormParser)  # Important pour les uploads

    @action(detail=True, methods=['post'], url_path='upload_photo')
    def upload_photo(self, request, pk=None):
        person = self.get_object()
        photo = request.FILES.get('photo')

        if photo:
            person.photo = photo
            person.save()
            return Response({'status': 'photo uploaded', 'photo_url': person.photo.url})
        else:
            return Response({'error': 'No photo uploaded'}, status=status.HTTP_400_BAD_REQUEST)

class FamilyRelationViewSet(viewsets.ModelViewSet):
    queryset = FamilyRelation.objects.all()
    serializer_class = FamilyRelationSerializer

@csrf_exempt
def run_algorithm(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        algo = data.get('algorithm')
        start_id = data.get('start_id')
        goal_id = data.get('goal_id')

        graph = build_graph()

        if algo == 'dfs':
            result = dfs(graph, start_id, goal_id)
        elif algo == 'bfs':
            result = bfs(graph, start_id, goal_id)
        elif algo == 'dijkstra':
            result = dijkstra(graph, start_id, goal_id)
        else:
            return JsonResponse({'error': 'Algorithme inconnu'}, status=400)

        return JsonResponse({'path': result})
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

