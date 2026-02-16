from django.shortcuts import render
from django.db.models import Sum, Count
from members.models import Member
from finance.models import Contribution, Loan, Fine
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
from django.http import HttpResponse
from django.conf import settings
import os


@login_required
def dashboard(request):
    total_members = Member.objects.count()

    savings_data = Contribution.objects.aggregate(Sum('amount'))
    total_savings = savings_data['amount__sum'] or 0.00

    active_loans_count = Loan.objects.filter(status='Active').count()

    loan_data = Loan.objects.filter(status='Active').aggregate(Sum('principal_amount'))
    total_loan_value = loan_data['principal_amount__sum'] or 0.00

    unpaid_fines = Fine.objects.filter(is_paid=False).count()


    recent_contributions = Contribution.objects.all().order_by('-date')[:5]
    recent_loans = Loan.objects.all().order_by('-issue_date')[:5]
    recent_fines = Fine.objects.all().order_by('-date_issued')[:5]

    # Combine them into one list
    # We create a new attribute 'type' for each so the template knows what they are
    for c in recent_contributions:
        c.type = 'Contribution'
        c.display_amount = c.amount
        c.common_date = c.date

    for l in recent_loans:
        l.type = 'Loan'
        l.display_amount = l.principal_amount
        l.common_date = l.issue_date

    for f in recent_fines:
        f.type = 'Fine'
        f.display_amount = f.amount
        f.common_date = f.date_issued


    activity_feed = sorted(
        chain(recent_contributions, recent_loans, recent_fines),
        key=attrgetter('common_date'),
        reverse=True
    )

    # Take the top 10 most recent events
    activity_feed = activity_feed[:10]

    context = {
        'total_members': total_members,
        'total_savings': total_savings,
        'active_loans_count': active_loans_count,
        'total_loan_value': total_loan_value,
        'unpaid_fines': unpaid_fines,
        'activity_feed': activity_feed,
    }

    return render(request, 'core/dashboard.html', context)

@login_required
def download_backup(request):
    # Path to db.sqlite3
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')

    if os.path.exists(db_path):
        with open(db_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/x-sqlite3")
            response['Content-Disposition'] = 'inline; filename=twelvefold_backup.sqlite3'
            return response
    else:
        return HttpResponse("Database not found", status=404)