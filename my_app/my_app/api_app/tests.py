from django.test import TestCase
from api_app.models import Nurse, Visit
# Create your tests here. ❯ python3 manage.py test

class NurseTestCase(TestCase):
    def setUp(self):
        self.nurse = Nurse(username="Mateusz",email="mateusz@dupa.pl", phone_number="123456789")

    def test_create_nurse(self): #czy tworzy nurse
        self.nurse.save()
        self.assertIsNotNone(self.nurse.id) #czy id jest rozne od 0

