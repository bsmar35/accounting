from api.constants import ApprovementState
from api.models import ApprovementBid
from api.serializers import ApprovementBidSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from django.db.models import Q


class ApprovementBidList(APIView):
    """
    List of approvement bids
    """
    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        bids = (ApprovementBid
                .objects
                .filter(~Q(state=ApprovementState.Closed)).order_by('created'))

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
