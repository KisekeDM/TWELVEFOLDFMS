from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Contribution
from .forms import ContributionForm
from .forms import LoanForm
from .models import Loan


def contribution_list(request):
    # Show latest contributions first
    contributions = Contribution.objects.all().order_by('-date')
    return render(request, 'finance/contribution_list.html', {'contributions': contributions})


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


def loan_list(request):
    loans = Loan.objects.all().order_by('-issue_date')
    return render(request, 'finance/loan_list.html', {'loans': loans})


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


def loan_detail(request, loan_id):
    loan = get_object_or_404(Loan, id=loan_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            loan.status = 'Active'
            loan.save()
            messages.success(request, f'Loan for {loan.member} has been APPROVED.')
        elif action == 'reject':
            loan.status = 'Rejected'
            loan.save()
            messages.warning(request, 'Loan application rejected.')

        return redirect('loan_list')

    return render(request, 'finance/loan_detail.html', {'loan': loan})