from django.urls import path
from .views import (
    login_page,
    dashboard,
    students_page,
    equipment_page,
    borrow_records_page
)

urlpatterns = [
    path('', login_page, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('students/', students_page, name='students'),
    path('equipment/', equipment_page, name='equipment'),
    path('borrow-records/', borrow_records_page, name='borrow_records'),
]