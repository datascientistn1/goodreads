from django.test import TestCase
from django.urls import reverse

from books.models import Book, BookReview
from users.models import CustomUser


class HomePagaTestCase(TestCase):
    def test_paginated_list(self):
        book=Book.objects.create(title='Book1',description='description1',isbn='isbn1')
        user = CustomUser.objects.create(
            username='nurzilola', first_name='Nurzilola', last_name="Maminova",email="nurzilola@gmail.com")

        user.set_password('nurzilola2004')
        user.save()
        review1=BookReview.objects.create(book=book,user=user,stars_given=3,comment="Very good book")
        review2=BookReview.objects.create(book=book,user=user,stars_given=4,comment="Useful book")
        review3=BookReview.objects.create(book=book,user=user,stars_given=5,comment="Nice book")

        response=self.client.get(reverse("home_page")+'?page_size=2')

        self.assertContains(response,review3.comment)
        self.assertContains(response,review2.comment)
        self.assertNotContains(response,review1.comment)

