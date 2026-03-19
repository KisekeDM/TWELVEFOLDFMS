from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import MemberForm
from .models import Member
from django.contrib.auth.decorators import login_required, user_passes_test
from finance.models import Fine
from decimal import Decimal
from .forms import MeetingForm
from .models import Meeting
from django.contrib.auth.models import User

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


@login_required
@user_passes_test(is_admin)
def edit_member(request, member_id):
    # Fetch the specific member
    member = get_object_or_404(Member, id=member_id)

    if request.method == 'POST':
        # Pass the existing member instance to the form
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f'{member.first_name}\'s profile updated successfully!')
            return redirect('member_list')
    else:
        # Pre-fill the form with the member's current data
        form = MemberForm(instance=member)

    # We can reuse the exact same member_form.html template!
    return render(request, 'members/member_form.html', {'form': form, 'is_edit': True})


@login_required
@user_passes_test(is_admin)
def pending_approvals(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')

        try:
            user_to_approve = User.objects.get(id=user_id)

            if action == 'approve':
                member_id = request.POST.get('member_id')
                if member_id:
                    member_profile = Member.objects.get(id=member_id)
                    member_profile.user = user_to_approve
                    member_profile.save()
                    messages.success(request,
                                     f"Successfully linked {user_to_approve.username} to {member_profile.first_name}.")
                else:
                    messages.error(request, "You must select a member profile to link.")

            elif action == 'reject':
                user_to_approve.delete()  # Delete the unauthorized user account
                messages.success(request, "User registration rejected and deleted.")

        except (User.DoesNotExist, Member.DoesNotExist):
            messages.error(request, "An error occurred. Please try again.")

        return redirect('pending_approvals')

    # Fetch users with no linked member profile
    pending_users = User.objects.filter(is_staff=False, member_profile__isnull=True)

    # Fetch members who do not have a user account linked yet
    available_members = Member.objects.filter(user__isnull=True)

    return render(request, 'members/pending_approvals.html', {
        'pending_users': pending_users,
        'available_members': available_members
    })