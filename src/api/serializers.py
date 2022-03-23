from ast import literal_eval
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Character, dump_character


def is_dict(s: str) -> bool:
    try:
        d = literal_eval(s)
    except Exception:
        return False
    return type(d) == dict


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password']
    
    def validate(self, attrs):
        # change password feature?
        #if "password" not in attrs:
        #    raise ValidationError("Missing password")
        return attrs

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.password != validated_data["password"]:
            instance.password = make_password(validated_data["password"])
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


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
        # print(self.context["request"].version)
        return Character.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user_id', instance.user)
        instance.data = validated_data.get('data', instance.data)
        instance.save()
        return instance