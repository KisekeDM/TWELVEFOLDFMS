from django.shortcuts import render, redirect
from django.db.models import Sum, Count
from members.models import Member
from finance.models import Contribution, Loan, Fine
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
from django.http import HttpResponse
from django.conf import settings
import os
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


@login_required
def dashboard(request):
    user = request.user
    is_admin = user.is_staff

    # Safely try to get the linked member profile (if it exists)
    member_profile = getattr(user, 'member_profile', None)

    # --- THE APPROVAL GATE ---
    if not is_admin and not member_profile:
        return render(request, 'core/pending_approval.html')

    # 1. KPI COUNTERS & RECENT DATA SELECTION
    total_members = Member.objects.count()  # Everyone sees total member count

    if is_admin:
        # ADMIN SEES EVERYTHING
        savings_data = Contribution.objects.aggregate(Sum('amount'))
        loan_data = Loan.objects.filter(status='Active').aggregate(Sum('principal_amount'))

        total_savings = savings_data['amount__sum'] or 0.00
        active_loans_count = Loan.objects.filter(status='Active').count()
        total_loan_value = loan_data['principal_amount__sum'] or 0.00
        unpaid_fines = Fine.objects.filter(is_paid=False).count()

        recent_contributions = Contribution.objects.all().order_by('-date')[:5]
        recent_loans = Loan.objects.all().order_by('-issue_date')[:5]
        recent_fines = Fine.objects.all().order_by('-date_issued')[:5]

    else:
        # REGULAR USER SEES ONLY THEIR DATA
        if member_profile:
            savings_data = Contribution.objects.filter(member=member_profile).aggregate(Sum('amount'))
            loan_data = Loan.objects.filter(member=member_profile, status='Active').aggregate(Sum('principal_amount'))

            total_savings = savings_data['amount__sum'] or 0.00
            active_loans_count = Loan.objects.filter(member=member_profile, status='Active').count()
            total_loan_value = loan_data['principal_amount__sum'] or 0.00
            unpaid_fines = Fine.objects.filter(member=member_profile, is_paid=False).count()

            recent_contributions = Contribution.objects.filter(member=member_profile).order_by('-date')[:5]
            recent_loans = Loan.objects.filter(member=member_profile).order_by('-issue_date')[:5]
            recent_fines = Fine.objects.filter(member=member_profile).order_by('-date_issued')[:5]
        else:
            # Fallback if the user hasn't been linked to a member profile yet
            total_savings = active_loans_count = total_loan_value = unpaid_fines = 0.00
            recent_contributions = recent_loans = recent_fines = []

    # 2. NORMALIZE AND MERGE ACTIVITY FEED
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
    )[:10]

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


def is_admin(user):
    return user.is_staff


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Account created successfully! Please log in. You will need Admin approval before accessing the system.')
            return redirect('login')  # Send them to the login page
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})