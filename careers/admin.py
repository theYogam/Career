from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Register your models here.


class LocationAdmin(admin.ModelAdmin):
    fields = ('town', 'country')
    list_display = ('town', 'country')
    # prepopulated_fields = {"slug": ("town",)}


class DomainAdmin(admin.ModelAdmin):
    fields = ('name', 'target', 'short_description')
    list_display = ('name', 'target', 'short_description')
    # prepopulated_fields = {"slug": ("name",)}


class OfferAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'position_count', 'domain', 'location')
    list_display = ('name', 'description', 'position_count', 'domain', 'location')
    # prepopulated_fields = {"slug": ("name",)}


class ApplicationAdmin(admin.ModelAdmin):
    fields = ('member', 'offer', 'resume', 'current_company', 'linkedin_url', 'github_url', 'portfolio_url',
              'other_website', 'facebook_url', 'instagram_url', 'youtube_url', 'additional_information', 'location', 'allowed_notifications')

    list_display = ('member', 'offer', 'current_company', 'linkedin_url', 'github_url', 'portfolio_url',
                    'other_website', 'facebook_url', 'instagram_url', 'youtube_url', 'additional_information', 'location', 'allowed_notifications')

    fieldsets = (
        (None, {'fields': ('offer', 'current_company', 'additional_information', 'allowed_notifications')}),
        (_('Identification'), {'fields': ('member', 'location')}),
        (_('Professional Links'), {'fields': ('linkedin_url', 'github_url', 'portfolio_url', 'other_website')}),
        (_('Social Links'), {'fields': ('facebook_url', 'instagram_url', 'youtube_url')})
    )

    readonly_fields = ('member', 'location')
