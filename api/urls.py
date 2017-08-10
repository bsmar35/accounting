from django.conf.urls import url
from api.views import accounts, managers

urlpatterns = [
    url(r'^accounts/register$', accounts.AccountRegister.as_view(), name='account_register'),
    url(r'^accounts/login$', accounts.AccountLogin.as_view(), name='account_login'),
    url(r'^accounts/(?P<pk>[0-9]+)/balance$', accounts.ViewAccountBalance.as_view(), name='account_balance'),
    url(r'^accounts/(?P<pk>[0-9]+)/leave_system', accounts.LeaveSystem.as_view(), name='leave_system'),
]


urlpatterns += [
    url(r'^managers/register$', managers.ApprovementBidList.as_view(), name='bids'),
    url(r'^managers/bids/(?P<pk>[0-9]+)', managers.ProcessApprovementBid.as_view(), name='process_bid'),
]
