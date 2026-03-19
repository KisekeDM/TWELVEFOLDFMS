from django.urls import path
from . import views

urlpatterns = [
    path('', views.member_list, name='member_list'),
    path('add/', views.add_member, name='add_member'),
    path('meetings/', views.meeting_list, name='meeting_list'),
    path('meetings/record/', views.record_meeting, name='record_meeting'),
    path('edit/<int:member_id>/', views.edit_member, name='edit_member'),
    path('pending/', views.pending_approvals, name='pending_approvals'),
]