from django.test import TestCase
from .models import Movie

# Create your tests here.
class MovieTests(TestCase):
    def test_generate_genres(self):
        bits = Movie.generate_genres("Hành động,Phiêu lưu")
        self.assertEqual(bits, 3)
        bits = Movie.generate_genres("Hoạt hình,Hài")
        self.assertEqual(bits, 12)
        bits = Movie.generate_genres("Tội phạm,Tâm lý")
        self.assertEqual(bits, 48)
        bits = Movie.generate_genres("Gia đình,Kinh dị")
        self.assertEqual(bits, 192)
