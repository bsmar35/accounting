from api.constants import ApprovementState
from api.models import ApprovementBid, Manager
from api.permissions import ManagerOnly
from api.serializers import ApprovementBidSerializer, ManagerLoginSerializer
from django.contrib.auth import login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ManagerLogin(APIView):
    """
    Login manager
    """

    def post(self, request):
        serializer = ManagerLoginSerializer(data=request.data)
        if not serializer.is_valid():
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        manager = Manager.objects.filter(**serializer.validated_data).first()
        if manager is not None:
            login(request, manager)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ApprovementBidList(APIView):
    """
    List of approvement bids
    """
    permission_classes = (ManagerOnly,)

    def get(self, request):
        bids = (ApprovementBid
                .objects
                .filter(processed__isnull=True).order_by('created'))

        serializer = ApprovementBidSerializer(bids, many=True)
        return Response(serializer.data)


class ProcessApprovementBid(APIView):
    """
    Process approvement bids
    """
    def post(self, request, pk):
        bid = ApprovementBid.objects.get(pk=pk)
        bid.process()
        return Response('Approvement processed', status=status.HTTP_200_OK)


class ClosedAccountsList(APIView):
    """
    List of approvement bids
    """
    permission_classes = (ManagerOnly,)

    def get(self, request):
        bids = (ApprovementBid
                .objects
                .filter(processed__isnull=False, state=ApprovementState.WaitingForDelete)
                .order_by('created')
                .select_related())

        accounts = [bid.account.to_dict() for bid in bids]
        return Response(accounts, status=status.HTTP_200_OK)
