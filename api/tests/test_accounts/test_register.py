from api.constants import AccountState, ApprovementState
from api.models import Account, ApprovementBid, AccountBalance
from django.test import TestCase, Client
from django.urls import reverse


class TestClients(TestCase):
    def setUp(self):
        self.client = Client()

    def test_success_client_register(self):
        """
        Test for success client registration
        """
        data = dict(
            first_name='Jack',
            last_name='Lindon',
            email='mail@mail.com',
            passport_number='sh112332'
        )

        response = self.client.post(reverse('account_register'), data)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.data.get('pin'))

        # check account data
        account = Account.objects.first()
        self.assertIsNotNone(account)
        self.assertEqual(account.state, AccountState.Inactive)
        self.assertEqual(account.first_name, 'Jack')
        self.assertEqual(account.last_name, 'Lindon')
        self.assertEqual(account.email, 'mail@mail.com')
        self.assertEqual(account.passport_number, 'sh112332')
        self.assertIsNotNone(account.pin)

        # check bid data
        bid = ApprovementBid.objects.first()
        self.assertEqual(bid.account, account)
        self.assertEqual(bid.state, ApprovementState.WaitingForActivate)

        # check balance data
        balance = AccountBalance.objects.first()
        self.assertEqual(balance.account, account)
        self.assertEqual(balance.balance, 0)
        self.assertEqual(balance.currency, 840)

    def test_fail_client_register(self):
        """
        Test for fail client registration
        """
        data = dict(
            last_name='Lindon',
            email='mail@mail.com',
            passport_number='sh112332'
        )

        response = self.client.post(reverse('account_register'), data)
        self.assertEqual(response.status_code, 400)
