from django.contrib import admin
from django.contrib.auth.models import Group

# Unregister the Groups model so it doesn't show up in the Admin panel
admin.site.unregister(Group)