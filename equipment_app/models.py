from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year_level = models.IntegerField()

    def __str__(self):
        return f"{self.student_id} - {self.name}"


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    total_quantity = models.IntegerField()
    available_quantity = models.IntegerField()

    def __str__(self):
        return self.name


class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ('Borrowed', 'Borrowed'),
        ('Returned', 'Returned'),
        ('Overdue', 'Overdue'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_borrowed = models.DateTimeField(auto_now_add=True)
    expected_return = models.DateField()
    date_returned = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Borrowed')

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be greater than zero.")

        if self.pk:
            old = BorrowRecord.objects.get(pk=self.pk)

            if self.quantity != old.quantity:
                raise ValidationError("Quantity cannot be edited after creation.")
        else:
            equipment = Equipment.objects.get(pk=self.equipment.pk)

            if self.quantity > equipment.available_quantity:
                raise ValidationError("Not enough equipment available.")

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        if not is_new:
            old = BorrowRecord.objects.get(pk=self.pk)
        else:
            old = None

        self.full_clean()

        super().save(*args, **kwargs)

        equipment = Equipment.objects.get(pk=self.equipment.pk)

        # New borrow
        if is_new:
            equipment.available_quantity -= self.quantity
            equipment.save()

        # Returned record cannot go back
        elif old.status == 'Returned' and self.status in ['Borrowed', 'Overdue']:
            raise ValidationError("Returned records cannot be changed back.")

        # Borrowed/Overdue -> Returned
        elif old.status in ['Borrowed', 'Overdue'] and self.status == 'Returned':
            equipment.available_quantity += self.quantity
            equipment.save()

            if not self.date_returned:
                self.date_returned = now().date()
                super().save(update_fields=['date_returned'])

    def __str__(self):
        return f"{self.student} - {self.equipment}"

def save(self, *args, **kwargs):
    is_new = self.pk is None

    self.full_clean()

    if is_new:
        super().save(*args, **kwargs)

        equipment = Equipment.objects.get(pk=self.equipment.pk)
        equipment.available_quantity -= self.quantity
        equipment.save()

    else:
        old = BorrowRecord.objects.get(pk=self.pk)

        # Block changing a returned record to another status
        if old.status == 'Returned' and self.status in ['Borrowed', 'Overdue']:
            raise ValidationError("Returned records cannot be changed back.")

        # Restore stock only once
        if old.status in ['Borrowed', 'Overdue'] and self.status == 'Returned':
            equipment = Equipment.objects.get(pk=self.equipment.pk)
            equipment.available_quantity += self.quantity
            equipment.save()

            if not self.date_returned:
                self.date_returned = now().date()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.equipment}"