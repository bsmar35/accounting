from api.models import Account
from api.serializers import AccountSerializer, AccountLoginSerializer
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions


class AccountRegister(APIView):
    """
    Register accounts
    """
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountLogin(APIView):
    """
    Login accounts
    """

    def post(self, request):
        serializer = AccountLoginSerializer(data=request.data)
        if not serializer.is_valid():
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        account = Account.objects.filter(**serializer.validated_data).first()
        if account is not None:
            if account.is_active:
                login(request, account)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response("Account isn't active", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ViewAccountBalance(APIView):
    """
    View account balances
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        account = Account.objects.get(pk=pk)
        balances = [balance.to_dict() for balance in account.balances.all()]
        return Response(balances, status=status.HTTP_200_OK)


class LeaveSystem(APIView):
    """
    Leave system bid
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        account = Account.objects.get(pk=pk)
        account.leave_system()
        return Response('Leaving system bid created', status=status.HTTP_200_OK)
