# -*- coding: utf-8 -*-
import django
from django.contrib import admin
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User

    def get_user_model():
        return User

from user_sessions.templatetags.user_sessions import device, location

from .models import Session


class ExpiredFilter(admin.SimpleListFilter):
    title = _('Is Valid')
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Active')),
            ('0', _('Expired'))
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(expire_date__gt=now())
        elif self.value() == '0':
            return queryset.filter(expire_date__lte=now())


class OwnerFilter(admin.SimpleListFilter):
    title = _('Owner')
    parameter_name = 'owner'

    def lookups(self, request, model_admin):
        return (
            ('my', _('Self')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'my':
            return queryset.filter(user=request.user)


class SessionAdmin(admin.ModelAdmin):
    list_display = 'ip', 'user', 'is_valid', 'location', 'device', 'last_activity',
    search_fields = ()
    list_filter = ExpiredFilter, OwnerFilter
    raw_id_fields = 'user',

    def __init__(self, *args, **kwargs):
        super(SessionAdmin, self).__init__(*args, **kwargs)
        if not self.search_fields and django.VERSION[:2] < (1, 7):
            self.search_fields = self.get_search_fields(None)

    def get_search_fields(self, request):
        User = get_user_model()
        return ('ip', 'user__%s' % getattr(User, 'USERNAME_FIELD', 'username'))

    def is_valid(self, obj):
        return obj.expire_date > now()
    is_valid.boolean = True

    def location(self, obj):
        return location(obj.ip)

    def device(self, obj):
        return device(obj.user_agent)

admin.site.register(Session, SessionAdmin)
