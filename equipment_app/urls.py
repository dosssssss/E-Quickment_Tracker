from django.urls import path
from .views import (
    login_page,
    logout_page,
    dashboard,
    students_page,
    add_student,
    edit_student,
    delete_student,
    equipment_page,
    add_equipment,
    borrow_records_page,
    return_borrow_record,
    add_borrow_record,
    edit_equipment
    
    
)

urlpatterns = [
    path('', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('students/', students_page, name='students'),
    path('students/add/', add_student, name='add_student'),
    path('equipment/', equipment_page, name='equipment'),
    path('equipment/add/', add_equipment, name='add_equipment'),
    path('borrow-records/', borrow_records_page, name='borrow_records'),
    path('borrow-records/add/', add_borrow_record, name='add_borrow_record'),
    path('students/edit/<int:student_id>/', edit_student, name='edit_student'),
    path('students/delete/<int:student_id>/', delete_student, name='delete_student'),
    path('borrow-records/return/<int:record_id>/', return_borrow_record, name='return_borrow_record'),
    path('equipment/edit/<int:item_id>/', edit_equipment, name='edit_equipment'),
]   