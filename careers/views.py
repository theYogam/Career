import json
import logging
from threading import Thread

from django.contrib import messages
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models.fields.files import FieldFile
from django.utils.translation import activate, ugettext as _
from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.db.models.fields.files import ImageFieldFile as DjangoImageFieldFile, FieldFile
from django.views.generic import TemplateView
from django.http.response import HttpResponseRedirect, Http404, HttpResponse, HttpResponseForbidden

from ikwen.core.generic import ChangeObjectBase
from ikwen.conf.settings import WALLETS_DB_ALIAS, MEDIA_URL, MEMBER_AVATAR
from ikwen.core.constants import MALE, FEMALE
from ikwen.core.models import Application, Service
from ikwen.core.fields import MultiImageFieldFile, ImageFieldFile
from ikwen.core.utils import add_database, get_service_instance, get_mail_content, send_sms, send_push, XEmailMessage, \
    get_preview_from_extension
from ikwen.core.views import HybridListView
from ikwen.accesscontrol.backends import UMBRELLA
from ikwen.accesscontrol.models import Member

from careers.admin import LocationAdmin, DomainAdmin, OfferAdmin, ApplicationAdmin
from careers.models import Location, Domain, Offer, Application
from conf import settings

logger = logging.getLogger('ikwen')


class Home(TemplateView):
    template_name = 'careers/home.html'

    def get(self, request, *args, **kwargs):
        domain = request.GET.get('domain')
        if domain:
            offer_list = [offer for offer in Offer.objects.filter(domain=domain)]
            return HttpResponse(json.dumps({'offer_list': offer_list}, 'content-type: text/json'))
        return super(Home, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['domain_list'] = [domain for domain in Domain.objects.all()]
        context['offer_list'] = [offer for offer in Offer.objects.all()]
        service = get_service_instance()
        context['service'] = service
        context['config'] = service.config
        context['user'] = self.request.user
        return context


class ShowOfferList(TemplateView):
    template_name = 'careers/show_offer_list.html'

    def get_context_data(self, **kwargs):
        context = super(ShowOfferList, self).get_context_data(**kwargs)
        context['offer_list'] = list(Offer.objects.all())
        service = get_service_instance()
        context['service'] = service
        context['config'] = service.config
        context['user'] = self.request.user
        return context


class OfferDetail(TemplateView):
    template_name = 'careers/offer_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OfferDetail, self).get_context_data(**kwargs)
        offer_slug = kwargs['offer_slug']
        context['offer'] = get_object_or_404(Offer, slug=offer_slug)
        service = get_service_instance()
        context['service'] = service
        context['config'] = service.config
        context['user'] = self.request.user
        return context


class ShowLocationList(TemplateView):
    template_name = 'careers/show_location_list.html'

    def get_context_data(self, **kwargs):
        context = super(ShowLocationList, self).get_context_data(**kwargs)
        location_list = []
        for location in Location.objects.all():
            offer_count = Offer.objects.filter(location=location).count()
            location.offer_count = offer_count
            location_list.append(location)
        context['location_list'] = location_list
        service = get_service_instance()
        context['service'] = service
        context['config'] = service.config
        context['user'] = self.request.user
        return context


class ShowDomainList(TemplateView):
    template_name = 'careers/show_domain_list.html'

    def get_context_data(self, **kwargs):
        context = super(ShowDomainList, self).get_context_data(**kwargs)
        domain_list = [domain for domain in Domain.objects.all()]
        for domain in domain_list:
            domain.available_offer_count = Offer.objects.filter(domain=domain).count()
        context['domain_list'] = domain_list
        service = get_service_instance()
        context['service'] = service
        context['config'] = service.config
        context['user'] = self.request.user
        return context


class ShowOfferPerLocation(TemplateView):
    template_name = 'careers/show_offer_per_location.html'

    def get_context_data(self, **kwargs):
        context = super(ShowOfferPerLocation, self).get_context_data(**kwargs)
        location_slug = kwargs['location_slug']
        location = Location.objects.get(slug=location_slug)
        context['offer_list'] = Offer.objects.filter(location=location)
        domain_list = [offer.domain for offer in Offer.objects.filter(location=location)]
        context['domain_count'] = len(set(domain_list))
        context['location'] = location
        return context


class ShowOfferPerDomain(TemplateView):
    template_name = 'careers/show_offer_per_domain.html'

    def get_context_data(self, **kwargs):
        context = super(ShowOfferPerDomain, self).get_context_data(**kwargs)
        domain_slug = kwargs['domain_slug']
        domain = get_object_or_404(Domain, slug=domain_slug)
        context['offer_list'] = Offer.objects.filter(domain=domain)
        location_list = [offer.location for offer in Offer.objects.filter(domain=domain)]
        context['location_count'] = len(set(location_list))
        context['domain'] = domain
        service = get_service_instance()
        context['service'] = service
        context['config'] = service.config
        context['user'] = self.request.user
        return context


class LocationList(HybridListView):
    model = Location
    model_admin = LocationAdmin


class ChangeLocation(ChangeObjectBase):
    model = Location
    model_admin = LocationAdmin
    label_field = 'town'


class DomainList(HybridListView):
    model = Domain
    model_admin = DomainAdmin


class ChangeDomain(ChangeObjectBase):
    model = Domain
    model_admin = DomainAdmin
    label_field = 'name'


class OfferSubmission(ChangeObjectBase):
    model = Application
    model_admin = ApplicationAdmin
    template_name = 'careers/offer_submission.html'

    def get_object(self, **kwargs):
        offer_slug = kwargs.get('offer_slug')
        offer = get_object_or_404(Offer, slug=offer_slug)
        try:
            application = Application.objects.get(member=self.request.user, offer=offer)
            return application
        except:
            pass

    def get_context_data(self, **kwargs):
        context = super(OfferSubmission, self).get_context_data(**kwargs)
        offer_slug = kwargs.get('offer_slug')
        context['offer'] = get_object_or_404(Offer, slug=offer_slug)
        context['location_list'] = [location for location in Location.objects.all()]
        service = get_service_instance()
        context['service'] = service
        context['config'] = service.config
        context['user'] = self.request.user
        return context

    def after_save(self, request, obj, *args, **kwargs):
        weblet = get_service_instance()
        offer_slug = kwargs.get('offer_slug')
        obj.member = request.user
        obj.save(using='default')
        staff_emails = [member.email for member in Member.objects.using(UMBRELLA).filter(is_staff=True)]

        subject = _("Thank you for your application")
        cta_url = "https://ikwen.com"
        applicant = obj.member
        try:
            html_content = get_mail_content(subject, template_name='careers/mails/thanks.html',
                                            extra_context={'applicant_name': applicant.full_name,
                                                           'offer': obj.offer,
                                                           'cta_url': cta_url})
            sender = 'Careers @ %s <no-reply@%s>' % (weblet.project_name, weblet.domain)
            msg = EmailMessage(subject, html_content, sender, [applicant.email])
            msg.bcc = staff_emails
            msg.content_subtype = "html"
            if getattr(settings, 'UNIT_TESTING', False):
                msg.send()
            else:
                Thread(target=lambda m: m.send(), args=(msg,)).start()
        except:
            logger.error("%s - Failed to send notice mail to %s." % (weblet, applicant.first_name), exc_info=True)
        body = _('Congratulation!!! We received your application for position as %(position)s' % {'position': obj.offer.name})
        send_push(weblet, applicant, subject, body, cta_url)
        return HttpResponseRedirect(reverse('careers:thanks', args=(offer_slug,)))


class OfferList(HybridListView):
    model = Offer
    model_admin = OfferAdmin


class ChangeOffer(ChangeObjectBase):
    model = Offer
    model_admin = OfferAdmin
    template_name = 'careers/change_offer.html'


class ApplicationList(HybridListView):
    model = Application
    model_admin = ApplicationAdmin
    list_filter = ('offer',)


class ChangeApplication(ChangeObjectBase):
    model = Application
    model_admin = ApplicationAdmin


class Thanks(TemplateView):
    template_name = 'careers/thanks.html'

    def get_context_data(self, **kwargs):
        context = super(Thanks, self).get_context_data(**kwargs)
        offer_slug = kwargs.get('offer_slug')
        context['offer'] = get_object_or_404(Offer, slug=offer_slug)
        service = get_service_instance()
        context['service'] = service
        context['config'] = service.config
        context['user'] = self.request.user
        return context






