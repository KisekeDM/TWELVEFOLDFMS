from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Contribution
from .forms import ContributionForm
from .forms import LoanForm
from .models import Loan
from .forms import RepaymentForm
from .forms import FineForm
from .models import Fine
from .forms import ReportFilterForm
from django.db.models import Sum
from decimal import Decimal
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_staff

@login_required
def contribution_list(request):
    if request.user.is_staff:
        contributions = Contribution.objects.all().order_by('-date')
    else:
        member = getattr(request.user, 'member_profile', None)
        contributions = Contribution.objects.filter(member=member).order_by('-date') if member else []

    return render(request, 'finance/contribution_list.html', {'contributions': contributions})

@login_required
@user_passes_test(is_admin)
def add_contribution(request):
    if request.method == 'POST':
        form = ContributionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contribution recorded successfully!')
            return redirect('contribution_list')
    else:
        form = ContributionForm()

    return render(request, 'finance/contribution_form.html', {'form': form})

@login_required
def loan_list(request):
    if request.user.is_staff:
        loans = Loan.objects.all().order_by('-issue_date')
    else:
        member = getattr(request.user, 'member_profile', None)
        loans = Loan.objects.filter(member=member).order_by('-issue_date') if member else []

    return render(request, 'finance/loan_list.html', {'loans': loans})

@login_required
def add_loan(request):
    if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            loan = form.save(commit=False)
            # The model default is 10%, but we can enforce it here if needed
            loan.interest_rate = 10.00
            loan.save()
            messages.success(request, 'Loan application submitted successfully!')
            return redirect('loan_list')
    else:
        form = LoanForm()

    return render(request, 'finance/loan_form.html', {'form': form})

@login_required
def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)
    repayment_form = RepaymentForm()  # Empty form for GET requests

    if request.method == 'POST':
        if 'repay' in request.POST:
            if 'action' in request.POST:
                if not request.user.is_staff:  # <--- Manual check inside the view
                    messages.error(request, "You do not have permission to approve loans.")
                    return redirect('loan_detail', loan_id=loan.id)
                if not request.user.is_staff:
                    messages.error(request, "You do not have permission to record repayments.")
                    return redirect('loan_detail', loan_id=loan.id)
            # Handle Repayment Submission
            form = RepaymentForm(request.POST)
            if form.is_valid():
                repayment = form.save(commit=False)
                repayment.loan = loan
                repayment.save()

                # Check if fully paid
                if loan.outstanding_balance <= 0:
                    loan.status = 'Paid'
                    loan.save()
                    messages.success(request, 'Loan fully repaid! Status updated to Paid.')
                else:
                    messages.success(request, 'Repayment recorded successfully.')
                return redirect('loan_detail', loan_id=loan.id)

        elif 'action' in request.POST:
            # Handle Approval/Rejection (Existing logic)
            action = request.POST.get('action')
            if action == 'approve':
                loan.status = 'Active'
                loan.save()
            elif action == 'reject':
                loan.status = 'Rejected'
                loan.save()
            return redirect('loan_list')

    return render(request, 'finance/loan_detail.html', {
        'loan': loan,
        'repayment_form': repayment_form
    })

@login_required
def fine_list(request):
    if request.user.is_staff:
        fines = Fine.objects.all().order_by('is_paid', '-date_issued')
    else:
        member = getattr(request.user, 'member_profile', None)
        fines = Fine.objects.filter(member=member).order_by('is_paid', '-date_issued') if member else []

    return render(request, 'finance/fine_list.html', {'fines': fines})

@login_required
@user_passes_test(is_admin)
def add_fine(request):
    if request.method == 'POST':
        form = FineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fine issued successfully!')
            return redirect('fine_list')
    else:
        form = FineForm()

    return render(request, 'finance/fine_form.html', {'form': form})



@login_required
@user_passes_test(is_admin)
def mark_fine_paid(request, fine_id):
    fine = get_object_or_404(Fine, id=fine_id)
    fine.is_paid = True
    fine.save()
    messages.success(request, f'Fine for {fine.member} marked as PAID.')
    return redirect('fine_list')

@login_required
def financial_report(request):
    selected_month = 'January'
    selected_year = 2026

    if request.method == 'GET' and 'month' in request.GET:
        form = ReportFilterForm(request.GET)
        if form.is_valid():
            selected_month = form.cleaned_data['month']
            selected_year = form.cleaned_data['year']
    else:
        form = ReportFilterForm(initial={'month': selected_month, 'year': selected_year})

    # 1. Calculate Total Contributions
    contributions = Contribution.objects.filter(month_paid_for=selected_month, date__year=selected_year)
    total_contributions = contributions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # 2. Calculate Loans Issued (Optional for now, but good to have)
    loans_issued = Loan.objects.filter(issue_date__month__gte=1, issue_date__year=selected_year)

    # 3. Calculate Fines Collected
    fines = Fine.objects.filter(date_issued__year=selected_year, is_paid=True)
    total_fines = fines.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')

    # 4. Net Balance Calculation (Now safe because both are Decimals)
    net_balance = total_contributions + total_fines

    context = {
        'form': form,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'total_contributions': total_contributions,
        'total_fines': total_fines,
        'net_balance': net_balance,
        'contributions': contributions,
    }

    return render(request, 'finance/financial_report.html', context)