# serializers.py
from rest_framework import serializers
from .models import Person, FamilyRelation
from rest_framework.views import APIView

from rest_framework import serializers

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        extra_kwargs = {
            'photo': {'required': False, 'allow_null': True}
        }


class FamilyRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyRelation
        fields = '__all__'


class PersonUpdateView(APIView):
    def put(self, request, pk):
        person = Person.objects.get(pk=pk)
        serializer = PersonSerializer(person, data=request.data, partial=True)

        if serializer.is_valid():
            # Si une nouvelle photo est envoyée dans la requête
            if 'photo' in request.FILES:
                photo_file = request.FILES['photo']
                person.update_photo(photo_file)  # Appel de la méthode pour mettre à jour la photo
                serializer.validated_data['photo'] = person.photo  # Met à jour le champ photo dans le serializer

            person.save()  # Sauvegarde les autres modifications
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)