from django.db import models
from django.conf import settings

class EmployeeSalary(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    salary_date = models.DateField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Expense(models.Model):
    category = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=[('Bank', 'Bank'), ('Cash', 'Cash')])
    vendor = models.CharField(max_length=100)
    invoice = models.FileField(upload_to='expenses/invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Income(models.Model):
    source = models.CharField(max_length=50)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    income_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=[('Bank', 'Bank'), ('Cash', 'Cash')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True)
    client_name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Overdue', 'Overdue')])

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client_name}"
    
class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name="items", on_delete=models.CASCADE)  # Links to the Invoice model
    description = models.CharField(max_length=255)  # Description of the product/service
    quantity = models.PositiveIntegerField()  # Quantity of the item
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Calculated total (quantity * unit_price)

    def save(self, *args, **kwargs):
        # Automatically calculate the total price before saving
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Item for Invoice {self.invoice.invoice_number}: {self.description}"