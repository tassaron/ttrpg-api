from django.urls import path
from . import views


urlpatterns = [
    path('character/<character_id>', views.get_character, name='get_character'),
]
