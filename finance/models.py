from django.db import models
from django.utils import timezone
from members.models import Member
from django.db.models import Sum


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

    # NEW FIELDS FOR "ON BEHALF" LOANS
    is_on_behalf = models.BooleanField(default=False, verbose_name="Applying on behalf of someone else?")
    beneficiary = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='benefited_loans', help_text="Leave blank if this loan is for you.")

    # Interest Rate (1-20%) [cite: 1083]
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.00)

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

    @property
    def total_repayment(self):
        rate_decimal = self.interest_rate / 100
        amount = float(self.principal_amount) * ((1 + float(rate_decimal)) ** self.duration_months)
        return round(amount, 2)

    @property
    def total_paid(self):
        total = self.repayments.aggregate(Sum('amount'))['amount__sum']
        return float(total) if total else 0.00

    @property
    def outstanding_balance(self):
        return round(self.total_repayment - self.total_paid, 2)

    @property
    def progress_percentage(self):
        # Calculate percentage for a progress bar
        if self.total_repayment == 0: return 0
        percent = (self.total_paid / self.total_repayment) * 100
        return int(percent)




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


class Repayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Repayment: {self.amount} for Loan #{self.loan.id}"