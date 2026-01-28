from django.core.management.base import BaseCommand
from transactions.models import RecurringTransaction, Transaction
from datetime import date
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = 'Process recurring transactions that are due'

    def handle(self, *args, **options):
        today = date.today()
        due_transactions = RecurringTransaction.objects.filter(next_date__lte=today)

        for rt in due_transactions:
            # Create a new transaction
            Transaction.objects.create(
                user=rt.user,
                type=rt.type,
                amount=rt.amount,
                category=rt.category,
                description=rt.description,
                date=rt.next_date
            )

            # Calculate the next date
            if rt.frequency == 'daily':
                rt.next_date += relativedelta(days=1)
            elif rt.frequency == 'weekly':
                rt.next_date += relativedelta(weeks=1)
            elif rt.frequency == 'monthly':
                rt.next_date += relativedelta(months=1)
            elif rt.frequency == 'yearly':
                rt.next_date += relativedelta(years=1)

            # If the next date is after the end date, delete the recurring transaction
            if rt.end_date and rt.next_date > rt.end_date:
                rt.delete()
            else:
                rt.save()

            self.stdout.write(self.style.SUCCESS(f'Processed recurring transaction: {rt.description}'))
