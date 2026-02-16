from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MemberForm
from .models import Member
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_staff

@login_required
def member_list(request):
    # Fetch all members to display in a table
    members = Member.objects.all().order_by('-date_joined')
    return render(request, 'members/member_list.html', {'members': members})

@login_required
@user_passes_test(is_admin)
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            # "success" message matches your Blue/Green theme
            messages.success(request, 'New member registered successfully!')
            return redirect('member_list')
    else:
        form = MemberForm()

    return render(request, 'members/member_form.html', {'form': form})