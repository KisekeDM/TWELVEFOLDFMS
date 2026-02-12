from django.shortcuts import render
from django.db.models import Sum, Count
from members.models import Member
from finance.models import Contribution, Loan, Fine


def dashboard(request):
    # 1. Total Members
    total_members = Member.objects.count()

    # 2. Total Savings (Sum of all contributions)
    # The 'aggregate' function returns a dictionary like {'amount__sum': 50000}
    savings_data = Contribution.objects.aggregate(Sum('amount'))
    total_savings = savings_data['amount__sum'] or 0.00

    # 3. Active Loans (Count of loans that are approved/active)
    active_loans_count = Loan.objects.filter(status='Active').count()

    # 4. Total Outstanding Loans (Sum of principal for active loans)
    # In a real app, you'd calculate (Principal + Interest) - Repayments.
    # For this MVP step, we sum the principal of active loans.
    loan_data = Loan.objects.filter(status='Active').aggregate(Sum('principal_amount'))
    total_loan_value = loan_data['principal_amount__sum'] or 0.00

    # 5. Pending Fines
    unpaid_fines = Fine.objects.filter(is_paid=False).count()

    context = {
        'total_members': total_members,
        'total_savings': total_savings,
        'active_loans_count': active_loans_count,
        'total_loan_value': total_loan_value,
        'unpaid_fines': unpaid_fines,
    }

    return render(request, 'core/dashboard.html', context)