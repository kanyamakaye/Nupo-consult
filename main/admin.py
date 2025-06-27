from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Partner, Service, TeamMember, Newsletter, ContactMessage

admin.site.register(Service)
admin.site.register(TeamMember)
admin.site.register(Newsletter)
admin.site.register(ContactMessage)
admin.site.register(Partner)
