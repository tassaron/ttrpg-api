from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.reverse import reverse_lazy
from rest_framework.response import Response
from .models import Character, dump_character
from ast import literal_eval


def is_dict(s: str) -> bool:
    try:
        d = literal_eval(s)
    except Exception:
        return False
    return type(d) == dict


class CharacterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Character
        fields = ['user_id', 'data']
    
    def validate(self, attrs):
        if attrs["data"] == "":
            attrs["data"] = dump_character()
        if not is_dict(attrs["data"]):
            raise ValidationError("The character data string must be a valid repr of a Python dict")
        return attrs

    def create(self, validated_data):
        return Character.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user_id', instance.user)
        instance.data = validated_data.get('data', instance.data)
        instance.save()
        return instance


class CharacterViewSet(viewsets.ModelViewSet):
    model = Character
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


    def list(self, request):
        all_data = []
        for row in self.queryset:
            serializer = self.serializer_class(row)
            data = serializer.data
            data.update({
                "url": reverse_lazy('api_v1:character-detail', args=[row.id], request=request)
            })
            all_data.append(data)
        return Response(all_data)


    def retrieve(self, request, pk=None):
        character = get_object_or_404(self.model, pk=pk)
        serializer = self.serializer_class(character)
        data = serializer.data
        data.update({
            "url": reverse_lazy('api_v1:character-detail', args=[pk], request=request)
        })
        return Response(data)


    def create(self, request):
        request.data["user_id"] = request.user.id
        serializer = self.serializer_class(self.queryset)
        data = serializer.validate(request.data)
        instance = serializer.create(data)
        return Response(self.serializer_class(instance).data)