from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from expenses.models import Expense
from .serializers import ExpenseSerializer
from rest_framework.pagination import PageNumberPagination

# Create your views here.
class ExpenseListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        expenses = Expense.objects.filter(user=request.user)
        if request.query_params.get('category'):
            expenses = expenses.filter(category=request.query_params['category'])
        if request.query_params.get('startDate'):
            expenses = expenses.filter(date__gte=request.query_params['startDate'])
        if request.query_params.get('endDate'):
            expenses = expenses.filter(date__lte=request.query_params['endDate'])

        result = paginator.paginate_queryset(expenses, request)
        serializer = ExpenseSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ExpenseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ExpenseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Expense.objects.get(pk=pk, user=self.request.user)
        except Expense.DoesNotExist:
            return None

    def get(self, request, pk):
        expense = self.get_object(pk)
        if expense is None:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    def put(self, request, pk):
        expense = self.get_object(pk)
        if expense is None:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ExpenseSerializer(expense, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        expense = self.get_object(pk)
        if expense is None:
            return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
        expense.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MonthlyExpenseSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = (
            Expense.objects.filter(user=request.user)
            .annotate(month=TruncMonth('date'))
            .values('month', 'category')
            .annotate(total=Sum('amount'))
            .order_by('month', 'category')
        )

        results = []
        for row in qs:
            month = row.get('month')
            month_str = month.strftime("%Y-%m") if month else "Unknown"
            results.append({
                "month": month_str,
                "category": row.get('category'),
                "total": row.get('total', 0)
            })
        return Response(results)