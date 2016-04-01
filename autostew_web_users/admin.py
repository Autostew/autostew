from django.contrib import admin

from autostew_web_users.models import SteamUser, SafetyClass

admin.site.register(SteamUser)
admin.site.register(SafetyClass)