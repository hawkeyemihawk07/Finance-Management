
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('transactions/', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),

    path('recurring/', views.recurring_transaction_list, name='recurring_transaction_list'),
    path('recurring/add/', views.add_recurring_transaction, name='add_recurring_transaction'),
    path('recurring/edit/<int:pk>/', views.edit_recurring_transaction, name='edit_recurring_transaction'),
    path('recurring/delete/<int:pk>/', views.delete_recurring_transaction, name='delete_recurring_transaction'),
]
