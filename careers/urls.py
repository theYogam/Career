
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required

from careers.views import Home, OfferDetail, ShowOfferList, OfferList, OfferSubmission, \
    ChangeOffer, ShowOfferPerDomain, ShowOfferPerLocation, ApplicationList, ChangeApplication, \
    ShowDomainList, DomainList, ChangeDomain, ShowLocationList, \
    LocationList, ChangeLocation, Thanks


urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='home'),

    url(r'^offers/$', ShowOfferList.as_view(), name='show_offer_list'),
    url(r'^(?P<offer_slug>[-\w]+)$', OfferDetail.as_view(), name='offer_detail'),
    url(r'^offers/domain/(?P<domain_slug>[-\w]+)$', ShowOfferPerDomain.as_view(), name='show_offer_per_domain'),
    url(r'^offers/location/(?P<location_slug>[-\w]+)$', ShowOfferPerLocation.as_view(), name='show_offer_per_location'),

    url(r'^domains/$', ShowDomainList.as_view(), name='show_domain_list'),
    url(r'^locations/$', ShowLocationList.as_view(), name='show_location_list'),
    url(r'^(?P<offer_slug>[-\w]+)/apply$', login_required(OfferSubmission.as_view()), name='offer_submission'),
    url(r'^(?P<offer_slug>[-\w]+)/thanks$', login_required(Thanks.as_view()), name='thanks'),

    url(r'^locationList/$', permission_required('careers.ik_manage_offer')(LocationList.as_view()), name='location_list'),
    url(r'^changeLocation/$', permission_required('careers.ik_manage_offer')(ChangeLocation.as_view()), name='change_location'),
    url(r'^changeLocation/(?P<object_id>[-\w]+)$', permission_required('careers.ik_manage_offer')(ChangeLocation.as_view()),
        name='change_location'),

    url(r'^domainList/$', permission_required('careers.ik_manage_offer')(DomainList.as_view()), name='domain_list'),
    url(r'^changeDomain/$', permission_required('careers.ik_manage_offer')(ChangeDomain.as_view()), name='change_domain'),
    url(r'^changeDomain/(?P<object_id>[-\w]+)$', permission_required('careers.ik_manage_offer')(ChangeDomain.as_view()),
        name='change_domain'),

    url(r'^offerList/$', permission_required('careers.ik_manage_offer')(OfferList.as_view()), name='offer_list'),
    url(r'^changeOffer/$', permission_required('careers.ik_manage_offer')(ChangeOffer.as_view()), name='change_offer'),
    url(r'^changeOffer/(?P<object_id>[-\w]+)$', permission_required('careers.ik_manage_offer')(ChangeOffer.as_view()),
        name='change_offer'),

    url(r'^applicationList/$', permission_required('careers.ik_manage_application')(ApplicationList.as_view()),
        name='application_list'),
    url(r'^changeApplication/$', permission_required('careers.ik_manage_application')(ChangeApplication.as_view()),
        name='change_application'),
    url(r'^changeApplication/(?P<object_id>[-\w]+)/$', permission_required('careers.ik_manage_application')
    (ChangeApplication.as_view()), name='change_application'),
)


