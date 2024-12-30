from rest_framework import serializers
from .models import EmployeeSalary, Expense, Income, Invoice, InvoiceItem

class EmployeeSalarySerializer(serializers.ModelSerializer):
    net_salary = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeSalary
        fields = [
            'id', 'employee', 'salary_date', 'basic_salary', 'allowances',
            'deductions', 'net_salary', 'status', 'created_at', 'updated_at'
        ]

    def get_net_salary(self, obj):
        return obj.basic_salary + obj.allowances - obj.deductions

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            'id', 'category', 'description', 'amount', 'payment_date',
            'payment_method', 'vendor', 'invoice', 'created_at', 'updated_at'
        ]

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Expense amount cannot be negative.")
        return value

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = [
            'id', 'source', 'description', 'amount', 'income_date',
            'payment_method', 'created_at', 'updated_at'
        ]

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Income amount cannot be negative.")
        return value

class InvoiceItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'quantity', 'unit_price', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.unit_price

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'client_name', 'issue_date', 'due_date',
            'total_amount', 'status', 'items'
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                InvoiceItem.objects.create(invoice=instance, **item_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def validate(self, data):
        if data['total_amount'] < 0:
            raise serializers.ValidationError("Total amount cannot be negative.")
        return data
