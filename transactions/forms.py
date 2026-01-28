
from django import forms
from .models import Transaction, Category, RecurringTransaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'amount', 'category', 'date', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class TransactionFilterForm(forms.Form):
    type = forms.ChoiceField(choices=[('', 'All'), ('income', 'Income'), ('expense', 'Expense')], required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    sort_by = forms.ChoiceField(choices=[('-date', 'Date (Newest First)'), ('date', 'Date (Oldest First)'), ('-amount', 'Amount (Highest First)'), ('amount', 'Amount (Lowest First)')], required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TransactionFilterForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

class RecurringTransactionForm(forms.ModelForm):
    class Meta:
        model = RecurringTransaction
        fields = ['type', 'amount', 'category', 'description', 'frequency', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RecurringTransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
