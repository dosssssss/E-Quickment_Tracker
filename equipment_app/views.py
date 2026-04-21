from django.shortcuts import render, redirect
from .models import Student, Equipment, BorrowRecord


def login_page(request):
    if request.method == "POST":
        return redirect('dashboard')
    return render(request, 'equipment_app/login.html')


def dashboard(request):
    context = {
        'students_count': Student.objects.count(),
        'equipment_count': Equipment.objects.count(),
        'borrowed_count': BorrowRecord.objects.filter(status='Borrowed').count(),
    }
    return render(request, 'equipment_app/dashboard.html', context)


def students_page(request):
    students = Student.objects.all()
    return render(request, 'equipment_app/students.html', {'students': students})


def equipment_page(request):
    items = Equipment.objects.all()
    return render(request, 'equipment_app/equipment.html', {'items': items})


def borrow_records_page(request):
    records = BorrowRecord.objects.all().order_by('-date_borrowed')
    return render(request, 'equipment_app/borrow_records.html', {'records': records})