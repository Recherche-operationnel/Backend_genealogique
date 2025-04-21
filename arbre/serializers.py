# serializers.py
from rest_framework import serializers
from .models import Person, FamilyRelation


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