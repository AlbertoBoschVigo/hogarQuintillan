from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

import datetime
# Create your tests here.


from .models import Memo

class MemoModelTests(TestCase):
    def test_today(self):
        # fecha_limite de hoy deberia saltar como True en day()
        time = timezone.now()
        memo_today = Memo(fecha_limite=time)
        self.assertIs(memo_today.day(), True)

    def test_tomorrow(self):
        # fecha_limite de mañana deberia saltar como False en day()
        time = timezone.now() + datetime.timedelta(days=1)
        memo_tomorrow = Memo(fecha_limite=time)
        self.assertIs(memo_tomorrow.day(), False)

    def test_this_week(self):
        # fecha_limite de hoy deberia saltar como True en week()
        time = timezone.now()
        memo_tomorrow = Memo(fecha_limite=time)
        self.assertIs(memo_tomorrow.week(), True)
    
    def test_next_week(self):
        # fecha_limite dentro de 7 dias deberia saltar como False en week()
        time = timezone.now() + datetime.timedelta(days=7)
        memo_tomorrow = Memo(fecha_limite=time)
        self.assertIs(memo_tomorrow.week(), False)

def create_memo(titulo, days, user):
    """
    Crea el memo y le asigna una fecha de creacion.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Memo.objects.create(titulo=titulo, detalle=titulo+'cuerpo del mensaje', fecha_limite=time, creador=user)


class MemoListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        User.objects.create_user(username='testuserfalso', password='12345')
    def test_no_memos(self):
        """
        If no memos exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('memos:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No hay memos disponibles.")
        self.assertQuerysetEqual(response.context['memo_list'], [])

    def test_past_memo(self):
        """
        memos with fecha_limite in the past are displayed on the
        index page.
        """
        user = User.objects.get(username='testuserfalso')
        create_memo(titulo="Past memo.", days=-30, user = user)
        response = self.client.get(reverse('memos:list'))
        self.assertQuerysetEqual(
            response.context['memo_list'],
            ['<Memo: Past memo.>']
        )

    def test_future_memo(self):
        """
        memos with a fecha_limte in the future are displayed too
        on the index page.
        """
        user = User.objects.get(username='testuserfalso')
        create_memo(titulo="Future memo.", days=30, user = user)
        response = self.client.get(reverse('memos:list'))
        #self.assertContains(response, "No hay memos disponibles.")
        self.assertQuerysetEqual(response.context['memo_list'], ['<Memo: Future memo.>'])

    def test_future_memo_and_past_memo(self):
        """
        If both past and future memos exist, first created
        is first displayed.
        """
        user = User.objects.get(username='testuserfalso')
        create_memo(titulo="Past memo.", days=-30, user = user)
        create_memo(titulo="Future memo.", days=30, user = user)
        response = self.client.get(reverse('memos:list'))
        self.assertQuerysetEqual(
            response.context['memo_list'],
            ['<Memo: Past memo.>', '<Memo: Future memo.>']
        )

    def test_two_past_memos(self):
        """
        The memos index page may display multiple memos.
        Return ordered by fecha_creacion
        """
        user = User.objects.get(username='testuserfalso')
        create_memo(titulo="Past memo 1.", days=-30, user = user)
        create_memo(titulo="Past memo 2.", days=-5, user = user)
        response = self.client.get(reverse('memos:list'))
        self.assertQuerysetEqual(
            response.context['memo_list'],
            ['<Memo: Past memo 1.>', '<Memo: Past memo 2.>']
        )