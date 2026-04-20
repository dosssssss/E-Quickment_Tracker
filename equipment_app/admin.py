from django.contrib import admin
from .models import Student, Equipment, BorrowRecord


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'course', 'year_level')
    search_fields = ('student_id', 'name', 'course')
    ordering = ('student_id',)


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_quantity', 'available_quantity')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'equipment',
        'quantity',
        'status',
        'date_borrowed',
        'expected_return',
        'date_returned',
    )
    search_fields = (
        'student__student_id',
        'student__name',
        'equipment__name',
    )
    list_filter = ('status', 'equipment')
    ordering = ('-date_borrowed',)