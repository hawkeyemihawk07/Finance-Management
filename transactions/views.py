
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, Category, RecurringTransaction
from .forms import TransactionForm, CategoryForm, TransactionFilterForm, RecurringTransactionForm
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def dashboard(request):
    total_income = Transaction.objects.filter(user=request.user, type='income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Transaction.objects.filter(user=request.user, type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expenses

    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:5]

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': balance,
        'recent_transactions': recent_transactions
    }
    return render(request, 'transactions/dashboard.html', context)




@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    form = TransactionFilterForm(request.GET, user=request.user)

    if form.is_valid():
        if form.cleaned_data['type']:
            transactions = transactions.filter(type=form.cleaned_data['type'])
        if form.cleaned_data['category']:
            transactions = transactions.filter(category=form.cleaned_data['category'])
        if form.cleaned_data['start_date']:
            transactions = transactions.filter(date__gte=form.cleaned_data['start_date'])
        if form.cleaned_data['end_date']:
            transactions = transactions.filter(date__lte=form.cleaned_data['end_date'])
        if form.cleaned_data['sort_by']:
            transactions = transactions.order_by(form.cleaned_data['sort_by'])
        else:
            transactions = transactions.order_by('-date')

    context = {
        'transactions': transactions,
        'form': form
    }
    return render(request, 'transactions/transaction_list.html', context)

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'transactions/add_transaction.html', {'form': form})

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction, user=request.user)
    return render(request, 'transactions/edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    messages.success(request, 'Transaction deleted successfully!')
    return redirect('transaction_list')

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'transactions/category_list.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'transactions/category_form.html', {'form': form})

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'transactions/category_form.html', {'form': form, 'category': category})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'transactions/category_confirm_delete.html', {'category': category})

@login_required
def recurring_transaction_list(request):
    transactions = RecurringTransaction.objects.filter(user=request.user)
    return render(request, 'transactions/recurring_transaction_list.html', {'transactions': transactions})

@login_required
def add_recurring_transaction(request):
    if request.method == 'POST':
        form = RecurringTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.next_date = transaction.start_date
            transaction.save()
            messages.success(request, 'Recurring transaction added successfully!')
            return redirect('recurring_transaction_list')
    else:
        form = RecurringTransactionForm(user=request.user)
    return render(request, 'transactions/recurring_transaction_form.html', {'form': form})

@login_required
def edit_recurring_transaction(request, pk):
    transaction = get_object_or_404(RecurringTransaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RecurringTransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recurring transaction updated successfully!')
            return redirect('recurring_transaction_list')
    else:
        form = RecurringTransactionForm(instance=transaction, user=request.user)
    return render(request, 'transactions/recurring_transaction_form.html', {'form': form, 'transaction': transaction})

@login_required
def delete_recurring_transaction(request, pk):
    transaction = get_object_or_404(RecurringTransaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Recurring transaction deleted successfully!')
        return redirect('recurring_transaction_list')
    return render(request, 'transactions/recurring_transaction_confirm_delete.html', {'transaction': transaction})
