from api.constants import ApprovementState, AccountState
from api.models import Account, ApprovementBid
from django.test import TestCase, Client
from django.urls import reverse


class TestApprovementList(TestCase):
    def setUp(self):

        self.acc1 = Account.new(
            first_name='Jack',
            last_name='Lindon',
            email='mail@mail.com',
            passport_number='sh112332'
        )

        self.acc2 = Account.new(
            first_name='Adam',
            last_name='Ginger',
            email='mail_a@mail.com',
            passport_number='8845'
        )

        ApprovementBid.objects.create(account=self.acc1, state=ApprovementState.WaitingForDelete)
        ApprovementBid.objects.create(account=self.acc1, state=ApprovementState.Closed)

        self.client = Client()

    def test_get_approvement_list(self):
        """
        Test for account leave system
        """
        response = self.client.get(reverse('bids'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 3)

        self.assertEqual(response.data[0].get('account'), self.acc1.id)
        self.assertEqual(response.data[0].get('state'), ApprovementState.WaitingForActivate)

        self.assertEqual(response.data[1].get('account'), self.acc2.id)
        self.assertEqual(response.data[1].get('state'), ApprovementState.WaitingForActivate)

        self.assertEqual(response.data[2].get('account'), self.acc1.id)
        self.assertEqual(response.data[2].get('state'), ApprovementState.WaitingForDelete)


class TestApprovementDetail(TestCase):
    def setUp(self):
        self.client = Client()

    def test_for_activate_account(self):
        """
        Test for account leave system
        """
        self.acc = Account.new(
            first_name='Jack',
            last_name='Lindon',
            email='mail@mail.com',
            passport_number='sh112332'
        )

        response = self.client.post(reverse('process_bid', args=[1]))
        self.assertEqual(response.status_code, 200)

        account = Account.objects.first()
        self.assertEqual(account.state, AccountState.Active)

        bid = ApprovementBid.objects.first()
        self.assertIsNotNone(bid.processed)
        self.assertEqual(bid.state, ApprovementState.Closed)
