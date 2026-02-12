from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'monthly_contribution_amount', 'is_active')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ('is_active', 'date_joined')