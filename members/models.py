from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='member_profile')

    # Matches SDS D1: Members
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # Phone number validation format as per SRS requirements [cite: 1083]
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        help_text="Format: 07XX XXX XXX"
    )

    # "Joining Date" [cite: 1248]
    date_joined = models.DateField(default=timezone.now)

    # Default contribution is KES 1000 based on SRS sample data [cite: 1248]
    monthly_contribution_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)

    # Status to handle "Deactivate Member" requirement [cite: 868]
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['first_name']

class Meeting(models.Model):
    date = models.DateField(default=timezone.now)
    title = models.CharField(max_length=100, default="Monthly General Meeting")
    # ManyToMany lets us select multiple members who attended
    attendees = models.ManyToManyField(Member, blank=True, related_name="meetings_attended")

    def __str__(self):
        return f"{self.title} - {self.date}"