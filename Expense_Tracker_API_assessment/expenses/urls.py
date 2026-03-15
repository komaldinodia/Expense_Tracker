from django.urls import path
from .views import ExpenseListCreateView, ExpenseDetailView, MonthlyExpenseSummaryView

urlpatterns = [
    path('', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('summary/', MonthlyExpenseSummaryView.as_view(), name='monthly-expense-summary'),
]