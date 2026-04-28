from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Equipment, BorrowRecord


def login_page(request):
    error = None

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid admin credentials."

    return render(request, 'equipment_app/login.html', {'error': error})


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/')
def dashboard(request):
    recent_records = BorrowRecord.objects.all().order_by('-date_borrowed')[:5]

    context = {
        'students_count': Student.objects.count(),
        'equipment_count': Equipment.objects.count(),
        'borrowed_count': BorrowRecord.objects.filter(status='Borrowed').count(),
        'overdue_count': BorrowRecord.objects.filter(status='Overdue').count(),
        'recent_records': recent_records,
    }

    return render(request, 'equipment_app/dashboard.html', context)


@login_required(login_url='/')
def students_page(request):
    students = Student.objects.all()
    return render(request, 'equipment_app/students.html', {'students': students})


@login_required(login_url='/')
def equipment_page(request):
    items = Equipment.objects.all()
    return render(request, 'equipment_app/equipment.html', {'items': items})


@login_required(login_url='/')
def borrow_records_page(request):
    records = BorrowRecord.objects.all().order_by('-date_borrowed')
    return render(request, 'equipment_app/borrow_records.html', {'records': records})

@login_required(login_url='/')
def return_borrow_record(request, record_id):
    record = BorrowRecord.objects.get(id=record_id)
    record.status = 'Returned'
    record.save()
    return redirect('borrow_records')

@login_required(login_url='/')
def add_student(request):
    if request.method == "POST":
        Student.objects.create(
            student_id=request.POST['student_id'],
            name=request.POST['name'],
            course=request.POST['course'],
            year_level=request.POST['year_level']
        )
        return redirect('students')

    return render(request, 'equipment_app/add_student.html')

@login_required(login_url='/')
def edit_student(request, student_id):
    student = Student.objects.get(id=student_id)

    if request.method == "POST":
        student.student_id = request.POST['student_id']
        student.name = request.POST['name']
        student.course = request.POST['course']
        student.year_level = request.POST['year_level']
        student.save()

        return redirect('students')

    return render(request, 'equipment_app/edit_student.html', {'student': student})

@login_required(login_url='/')
def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    student.delete()
    return redirect('students')

@login_required(login_url='/')
def add_equipment(request):
    if request.method == "POST":
        Equipment.objects.create(
            name=request.POST['name'],
            total_quantity=request.POST['total_quantity'],
            available_quantity=request.POST['available_quantity']
        )
        return redirect('equipment')
    
    
    return render(request, 'equipment_app/add_equipment.html')
@login_required(login_url='/')
def edit_equipment(request, item_id):
    item = Equipment.objects.get(id=item_id)

    if request.method == "POST":
        item.name = request.POST['name']
        item.total_quantity = request.POST['total_quantity']
        item.available_quantity = request.POST['available_quantity']
        item.save()

        return redirect('equipment')

    return render(request, 'equipment_app/edit_equipment.html', {'item': item})

@login_required(login_url='/')
def add_borrow_record(request):
    if request.method == "POST":
        BorrowRecord.objects.create(
            student_id=request.POST['student'],
            equipment_id=request.POST['equipment'],
            quantity=request.POST['quantity'],
            expected_return=request.POST['expected_return'],
            status='Borrowed'
        )
        return redirect('borrow_records')

    students = Student.objects.all()
    items = Equipment.objects.all()

    context = {
        'students': students,
        'items': items
    }

    return render(request, 'equipment_app/add_borrow_record.html', context)