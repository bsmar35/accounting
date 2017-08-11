from api.models import Account, ApprovementBid
from django.forms import model_to_dict
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'email', 'passport_number')
        extra_kwargs = {'first_name': {'required': True}}

    def create(self, validated_data):
        account = Account.new(validated_data.get('first_name'),
                              validated_data.get('last_name'),
                              validated_data.get('email'),
                              validated_data.get('passport_number'))

        return model_to_dict(account)


class AccountLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'pin')


class ApprovementBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovementBid
        fields = ('created', 'state', 'account')


class ManagerLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password')
