from api.models import Account, AccountBalance
from django.test import TestCase, Client
from django.urls import reverse


class TestBalance(TestCase):
    def setUp(self):
        self.client = Client()
        self.acc = Account.objects.create(
            first_name='Jack',
            last_name='Lindon',
            email='mail@mail.com',
            passport_number='sh112332',
            pin=8527
        )

        AccountBalance.objects.create(
            account=self.acc,
            currency=980,
            balance=100
        )

        AccountBalance.objects.create(
            account=self.acc,
            currency=840,
            balance=1200
        )

    def test_success_client_login(self):
        """
        Test for success client login
        """
        data = dict(email='mail@mail.com', pin=8527)
        response = self.client.post(reverse('account_login'), data)
        self.assertEqual(response.status_code, 200)

    def test_success_client_balance_view(self):
        """
        Test for success client registration
        """
        data = dict(email='mail@mail.com', pin=8527)
        self.client.post(reverse('account_login'), data)
        response = self.client.get(reverse('account_balance', args=[self.acc.id]))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('balance'), 100)
        self.assertEqual(response.data[0].get('currency'), 980)

        self.assertEqual(response.data[1].get('balance'), 1200)
        self.assertEqual(response.data[1].get('currency'), 840)

    def test_without_login_balance_view(self):
        """
        Test for retrieve balance info without login
        """
        response = self.client.get(reverse('account_balance', args=[self.acc.id]))
        self.assertEqual(response.status_code, 403)
