from datetime import datetime
from api.constants import AccountState, ApprovementState
from django.contrib.auth.models import User
from django.db import models
from random import randint
from django.db import transaction


class Account(User):
    passport_number = models.CharField(max_length=25)
    updated = models.DateTimeField(null=True)
    state = models.SmallIntegerField(default=1)
    pin = models.IntegerField()

    def __unicode__(self):
        return u'{}'.format(self.email)

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

        return account

    @transaction.atomic
    def leave_system(self):
        self.state = AccountState.Inactive
        self.save()

        ApprovementBid.objects.create(
            account=self,
            state=ApprovementState.WaitingForDelete
        )


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
        if self.state == ApprovementState.WaitingForActivate:
            self.account.state = AccountState.Active
        elif self.state == ApprovementState.WaitingForDelete:
            self.account.state = ApprovementState.Closed

        self.account.save()
        self.processed = datetime.now()
        self.state = ApprovementState.Closed
        self.save()


class AccountBalance(models.Model):
    account = models.ForeignKey(Account, related_name='balances')
    currency = models.IntegerField()
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def to_dict(self):
        return {"currency": self.currency, "balance": self.balance}
