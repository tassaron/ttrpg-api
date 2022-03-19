from django.db import models
from django.contrib.auth.models import User
from dnd_character import Character as DND_Character
from ast import literal_eval
from typing import Optional


def dump_character(character: Optional[DND_Character] = None) -> str:
    if character is None:
        character = DND_Character()
    return str(dict(character))


def load_character(character_data: str) -> DND_Character:
    return DND_Character(**literal_eval(character_data))


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.CharField(max_length=5000, default=dump_character)

    def set_character(self, character: DND_Character) -> bool:
        try:
            self.data = dump_character(character)
            return True
        except Exception as e:
            # log e
            return False

    def get_character(self) -> DND_Character:
        return load_character(self.data)

    def get_character_data(self) -> dict:
        return literal_eval(self.data)

    def __str__(self):
        return self.__class__.__qualname__