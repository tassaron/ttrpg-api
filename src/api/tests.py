from django.test import TestCase
from django.contrib.auth.models import User
from .models import Character

class AnimalTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testificate", password="diamond")
        self.character = Character.objects.create(user=self.user)

    def test_character_can_level_up(self):
        """Character can be hydrated and increase level using experience points"""
        hydrated_character = self.character.get_character()
        hydrated_character.experience += hydrated_character.experience.to_next_level
        self.assertEqual(hydrated_character.level, 2)

    def test_character_owned_by_first_user(self):
        """Character should be owned by user 1"""
        character = Character.objects.get(id=self.character.id)
        self.assertEqual(character.user_id, self.user.id)

    def test_character_not_owned_by_second_user(self):
        """Character should not be owned by user 2"""
        user2 = User.objects.create(username="villager", password="emerald")
        self.assertNotEqual(self.character.user_id, user2.id)
