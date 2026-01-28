from django.db import migrations

def add_categories(apps, schema_editor):
    Category = apps.get_model('transactions', 'Category')
    User = apps.get_model('auth', 'User')

    users = User.objects.all()

    if users.exists():
        categories_to_add = ['Food', 'Transport', 'Utilities', 'Entertainment', 'Salary']
        for user in users:
            for category_name in categories_to_add:
                Category.objects.get_or_create(user=user, name=category_name)
    else:
        pass

def remove_categories(apps, schema_editor):
    Category = apps.get_model('transactions', 'Category')
    User = apps.get_model('auth', 'User')

    users = User.objects.all()
    if users.exists():
        categories_to_remove = ['Food', 'Transport', 'Utilities', 'Entertainment', 'Salary']
        for user in users:
            Category.objects.filter(user=user, name__in=categories_to_remove).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(add_categories, remove_categories),
    ]