from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test, permission_required

from ikwen.core.views import Offline

from ikwen_kakocase.kakocase.views import AdminHome, MerchantList, Welcome, GuardPage, FirstTime
from ikwen_webnode.webnode.views import FlatPageView


from website.views import About, Webnode, Kakocase, Shavida, PinsView, Terms, Bundle, ServiceIndexes
from careers.views import Home

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^laakam/', include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^offline.html$', Offline.as_view(), name='offline'),
    url(r'^about$', About.as_view(), name='about'),
    url(r'^support_bundle$', Bundle.as_view(), name='support_bundle'),
    url(r'^terms$', Terms.as_view(), name='terms_and_conditions'),
    url(r'^billing/', include('ikwen.billing.urls', namespace='billing')),
    url(r'^cashout/', include('ikwen.cashout.urls', namespace='cashout')),
    url(r'^trade/', include('ikwen_kakocase.trade.urls', namespace='trade')),
    url(r'^billing/', include('ikwen.billing.urls', namespace='billing')),
    url(r'^cashout/', include('ikwen.cashout.urls', namespace='cashout')),
    url(r'^marketing/', include('ikwen_kakocase.commarketing.urls', namespace='marketing')),
    url(r'^sales/', include('ikwen_kakocase.sales.urls', namespace='sales')),
    url(r'^shopping/', include('ikwen_kakocase.shopping.urls', namespace='shopping')),
    url(r'^theming/', include('ikwen.theming.urls', namespace='theming')),
    url(r'^serviceIndexes/(?P<start>[\d]+)/$', ServiceIndexes.as_view(), name='service_indexes'),
    url(r'^webnode/$', Webnode.as_view(), name='webnode'),
    url(r'^kakocase/$', Kakocase.as_view(), name='kakocase'),
    # url(r'^shavida/$', Shavida.as_view(), name='shavida'),
    url(r'^pinsview/$', PinsView.as_view(), name='pinsview'),
    url(r'^revival/', include('ikwen.revival.urls', namespace='revival')),
    url(r'^ikwen/', include('ikwen.core.urls', namespace='ikwen')),

    # Foulassi URLs
    url(r'^foulassi/', include('ikwen_foulassi.foulassi.urls', namespace='foulassi')),

    url(r'^page/(?P<url>[-\w]+)/$', FlatPageView.as_view(), name='flatpage'),
    url(r'^blog/', include('ikwen_webnode.blog.urls', namespace='blog')),
    url(r'^web/', include('ikwen_webnode.web.urls', namespace='web')),
    url(r'^items/', include('ikwen_webnode.items.urls', namespace='items')),
    url(r'^echo/', include('echo.urls', namespace='echo')),

    url(r'^daraja/', include('daraja.urls', namespace='daraja')),
    url(r'^guardPage/$', GuardPage.as_view(), name='guard_page'),

    url(r'^$', Home.as_view(), name='home'),
    url(r'^', include('careers.urls', namespace='careers')),

)
