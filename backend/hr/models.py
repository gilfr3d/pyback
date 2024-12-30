from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")
    salary = models.CharField(max_length=15, blank=True)
    date_joined = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name}"

class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="leaves")
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()

    def __str__(self):
        return f"{self.employee} - {self.start_date} to {self.end_date}"

