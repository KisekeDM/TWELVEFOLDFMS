from django.contrib import admin
from .models import Contribution, Loan, Fine

admin.site.register(Contribution)
admin.site.register(Loan)
admin.site.register(Fine)
