from django.db import models
from django.db.models import Model
from django.template.defaultfilters import slugify
from django.utils.translation import gettext as _, get_language
# from django.contrib.gis.utils import GeoIP

from ikwen.accesscontrol.models import Member
from ikwen.core.fields import FileField, FieldFile
from ikwen.core.models import Country


class Location(Model):
    UPLOAD_TO = 'careers/Locations'
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    town = models.CharField(max_length=150)
    country = models.ForeignKey(Country)
    cover_image = models.ImageField(_('Cover image'),
                                    help_text=_('Upload a cover image which help to illustrates the location'),
                                    upload_to=UPLOAD_TO, null=True)

    def __unicode__(self):
        return "%s, %s" % (self.town, self.country)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.slug = slugify(self.__unicode__())
        super(Location, self).save()


class Domain(Model):
    UPLOAD_TO = 'careers/Domains'
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    cover_image = models.ImageField(_('Cover image'),
                                    help_text=_('Upload a cover image which help to illustrates the domain'), upload_to=UPLOAD_TO)
    short_description = models.TextField(_("Small description"), blank=True, null=True)
    target = models.CharField(_("Target reason"), max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.slug = slugify(self.name)
        super(Domain, self).save()


class Offer(Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)
    description = models.TextField()
    position_count = models.IntegerField(default=1)
    domain = models.ForeignKey(Domain)
    location = models.ForeignKey(Location)

    def __unicode__(self):
        return self.slug
    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.id:
            self.slug = slugify(self.name)
        super(Offer, self).save()


class Application(Model):
    upload_to = 'careers/Applications'
    member = models.ForeignKey(Member)
    offer = models.ForeignKey(Offer, help_text=_('Position to which you apply'))
    allowed_notifications = models.BooleanField(help_text=_('Does applicant which '
                                                           'to be notified for future job opportunities'),
                                               default=False, editable=True, null=True, blank=True)
    resume = FileField(verbose_name=_('Resume or CV'), allowed_extensions=['pdf', 'doc'],
                       upload_to=upload_to, help_text=_('Upload your resume or CV here'))
    current_company = models.CharField(_('Name of the current company'), max_length=100,
                                       help_text=_('Name of the company you are currently working in'), null=True, blank=True)

    linkedin_url = models.URLField(_('LinkedIn URL'), null=True, blank=True)
    github_url = models.URLField(_('Github URL'), null=True, blank=True)
    portfolio_url = models.URLField(_('Link to your Portfolio'), null=True, blank=True)
    other_website = models.URLField(_('Other website URL'), null=True, blank=True)

    facebook_url = models.URLField(_('Facebook URL'), null=True, blank=True)
    instagram_url = models.URLField(_('Instagram URL'), null=True, blank=True)
    twitter_url = models.URLField(_('Twitter URL'), null=True, blank=True)
    youtube_url = models.URLField(_('YouTube URL'), null=True, blank=True)

    additional_information = models.TextField(_('Additional information'), null=True, blank=True,
                                              help_text=_('Add cover letter or anything else you want to share'))
    location = models.ForeignKey(_('Location'),
                                 help_text=_('Put the correct area and city where you live separated by a comma'),
                                 blank=True, null=True)

    def __unicode__(self):
        return "%(applicant_name)s: %(offer)s" %\
               {'applicant_name': self.member.first_name, 'offer': self.offer}
    # g = GeoIP()
    # ip = request.META.get('REMOTE_ADDR', None)
    # if ip:
    #     city = g.city(ip)['city']
    # else:
    #     city = 'Rome'  # default city