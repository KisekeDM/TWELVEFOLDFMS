from django.db import models
from django.utils import timezone
from members.models import Member  # Link to the Member app


# --- 1. CONTRIBUTION MODEL (Matches SDS D2: Transactions) [cite: 465] ---
class Contribution(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    # To track which month this payment is for (e.g., "January") [cite: 1256]
    month_paid_for = models.CharField(
        max_length=20,
        choices=[
            ('January', 'January'), ('February', 'February'), ('March', 'March'),
            ('April', 'April'), ('May', 'May'), ('June', 'June'),
            ('July', 'July'), ('August', 'August'), ('September', 'September'),
            ('October', 'October'), ('November', 'November'), ('December', 'December')
        ]
    )

    def __str__(self):
        return f"{self.member} - {self.amount} ({self.month_paid_for})"


# --- 2. LOAN MODEL (Matches SDS D3: Loans) [cite: 466] ---
class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    principal_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Interest Rate (1-20%) [cite: 1083]
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=15.00)

    # Duration in months [cite: 1081]
    duration_months = models.IntegerField(default=1)

    issue_date = models.DateField(default=timezone.now)

    # Status tracking [cite: 1252]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Active', 'Active'),
        ('Paid', 'Paid'),
        ('Rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Loan: {self.member} - KES {self.principal_amount}"


# --- 3. FINE MODEL (Matches SDS D4: Fines) [cite: 467] ---
class Fine(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=100)  # e.g., "Late Payment", "Missed Meeting" [cite: 1254]
    date_issued = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Fine: {self.member} - {self.reason}"

    @property
    def total_repayment(self):
        # SDS Formula: Compound Interest = Principal * (1 + r/100)^n
        # We use the Decimal type for financial precision
        rate_decimal = self.interest_rate / 100
        amount = self.principal_amount * ((1 + rate_decimal) ** self.duration_months)
        return round(amount, 2)