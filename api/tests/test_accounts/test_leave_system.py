from api.constants import ApprovementState, AccountState
from api.models import Account, ApprovementBid
from django.test import TestCase, Client
from django.urls import reverse


class TestLeaveSystem(TestCase):
    def setUp(self):

        self.acc = Account.objects.create(
            first_name='Jack',
            last_name='Lindon',
            email='mail@mail.com',
            passport_number='sh112332',
            pin=8521,
            state=AccountState.Active
        )

        self.client = Client()
        data = dict(email='mail@mail.com', pin=8521)
        self.client.post(reverse('account_login'), data)

    def test_leave_system(self):
        """
        Test for account leave system
        """
        response = self.client.get(reverse('leave_system', args=[self.acc.id]))
        self.assertEqual(response.status_code, 200)

        bid = ApprovementBid.objects.first()
        self.assertEqual(bid.account, self.acc)
        self.assertEqual(bid.state, ApprovementState.WaitingForDelete)

        account = Account.objects.first()
        self.assertEqual(account.state, AccountState.Inactive)
