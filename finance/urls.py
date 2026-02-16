from django.urls import path
from . import views

urlpatterns = [
    path('contributions/', views.contribution_list, name='contribution_list'),
    path('contributions/add/', views.add_contribution, name='add_contribution'),

    path('loans/', views.loan_list, name='loan_list'),
    path('loans/add/', views.add_loan, name='add_loan'),

    path('loans/<int:loan_id>/', views.loan_detail, name='loan_detail'),

    path('fines/', views.fine_list, name='fine_list'),
    path('fines/add/', views.add_fine, name='add_fine'),
    path('fines/pay/<int:fine_id>/', views.mark_fine_paid, name='mark_fine_paid'),

    path('reports/', views.financial_report, name='financial_report'),
]