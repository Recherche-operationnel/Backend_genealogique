# views.py
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Person, FamilyRelation
from .serializers import PersonSerializer, FamilyRelationSerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser

@parser_classes([MultiPartParser, JSONParser])
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    parser_classes = (MultiPartParser, FormParser)  # Important pour les uploads

class FamilyRelationViewSet(viewsets.ModelViewSet):
    queryset = FamilyRelation.objects.all()
    serializer_class = FamilyRelationSerializer