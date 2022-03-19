from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Character


def get_character(request, character_id):
    character_row = get_object_or_404(Character, id=character_id)
    character_data = character_row.get_character_data()
    return JsonResponse(character_data)
