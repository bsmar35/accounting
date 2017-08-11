from datetime import datetime
from random import randint
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db import models
from django.db import transaction

from api.constants import AccountState, ApprovementState


class Account(User):
    passport_number = models.CharField(max_length=25)
    updated = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
    pin = models.IntegerField()

    def __unicode__(self):
        return u'{}'.format(self.email)

    @property
    def is_activated(self):
        return self.state == AccountState.Active

    @staticmethod
    @transaction.atomic
    def new(first_name, last_name, email, passport_number):
        account = Account.objects.create(
            username=email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            passport_number=passport_number,
            pin=randint(1000, 9999)
        )

        AccountBalance.objects.create(
            account=account,
            currency=840,
            balance=0
        )

        ApprovementBid.objects.create(
            account=account,
            state=ApprovementState.WaitingForActivate
        )

        send_mail('Approvement bid',
                  'New account',
                  'account_team@example.com',
                  [m.email for m in Manager.objects.all()],  # todo move to setting responsible manager
                  fail_silently=False)

        return account

    @transaction.atomic
    def leave_system(self):
        self.state = AccountState.Inactive
        self.save()

        ApprovementBid.objects.create(
            account=self,
            state=ApprovementState.WaitingForDelete
        )

        send_mail('Approvement bid',
                  'System leave',
                  'account_team@example.com',
                  [m.email for m in Manager.objects.all()],  # todo move to setting responsible manager
                  fail_silently=False)

    def to_dict(self):
        return dict(id=self.id,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    email=self.email,
                    state=self.state)


class Manager(User):
    def __unicode__(self):
        return u'{}'.format(self.email)


class ApprovementBid(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    state = models.SmallIntegerField()
    account = models.ForeignKey(Account)
    processed = models.DateTimeField(null=True)

    @transaction.atomic
    def process(self):
        message = ''
        if self.state == ApprovementState.WaitingForActivate:
            self.account.state = AccountState.Active
            message = 'Account activated'
        elif self.state == ApprovementState.WaitingForDelete:
            self.account.state = AccountState.Closed
            message = 'Account closed'

        self.account.save()
        self.processed = datetime.now()
        self.save()
        send_mail('Approvement',
                  message,
                  'account_team@example.com',
                  ['self.account.email'],
                  fail_silently=False)


class AccountBalance(models.Model):
    account = models.ForeignKey(Account, related_name='balances')
    currency = models.IntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def to_dict(self):
        return {"currency": self.currency, "balance": self.balance}
