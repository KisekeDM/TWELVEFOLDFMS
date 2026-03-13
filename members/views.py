from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MemberForm
from .models import Member
from django.contrib.auth.decorators import login_required, user_passes_test
from finance.models import Fine
from decimal import Decimal
from .forms import MeetingForm
from .models import Meeting

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


@login_required
def meeting_list(request):
    meetings = Meeting.objects.all().order_by('-date')
    return render(request, 'members/meeting_list.html', {'meetings': meetings})


@login_required
@user_passes_test(is_admin)  # Only Admins can record meetings
def record_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            # 1. Save the meeting and attendees
            meeting = form.save()

            # 2. Find who was ABSENT
            attendees = meeting.attendees.all()
            all_members = Member.objects.all()
            # Get members who are NOT in the attendees list
            absentees = all_members.exclude(id__in=attendees.values_list('id', flat=True))

            # 3. Automatically issue fines
            fines_created = 0
            for absentee in absentees:
                Fine.objects.create(
                    member=absentee,
                    amount=Decimal('100.00'),
                    reason=f"Absent from {meeting.title}",
                    date_issued=meeting.date,
                    is_paid=False
                )
                fines_created += 1

            messages.success(request,
                             f'Meeting recorded! {fines_created} members were automatically fined KES 100 for absenteeism.')
            return redirect('meeting_list')
    else:
        form = MeetingForm()

    return render(request, 'members/meeting_form.html', {'form': form})