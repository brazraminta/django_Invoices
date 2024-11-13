from django.urls import path
from . import views

# invoices/urls.py
urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('all/', views.all_invoices, name='all_invoices'),
    path('unpaid/', views.unpaid_invoices, name='unpaid_invoices'),
    path('register/', views.register_invoice_received, name='register_invoice_received'),
    path('filter_projects/', views.filter_projects, name='filter_projects'),
    path('filter_suppliers/', views.filter_suppliers, name='filter_suppliers'),
    path('invoices/clear/', views.clear_filters, name='clear_filters'),
    path('edit/<int:pk>/', views.edit_invoice, name='edit_invoice'),
    path('invoices/remove_pdf_link/<int:pk>/', views.remove_pdf_link, name='remove_pdf_link'),
    path('delete/<int:pk>/', views.delete_invoice, name='delete_invoice'),
    path('export/invoices/', views.export_invoices_to_excel, name='export_invoices_to_excel'),
    path('confirm/<int:pk>/', views.confirm_payment, name='confirm_payment'),
    path('create_invoice/', views.create_invoice_view, name='create_invoice'),
    path('generate_invoice_pdf/<int:pk>/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    path('download-backup/', views.download_backup, name='download_backup'),
]

