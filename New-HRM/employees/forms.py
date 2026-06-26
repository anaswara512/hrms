from django import forms
from .models import Employee
from accounts.models import User

class EmployeeForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(role='EMPLOYEE'),
        required=False,
        empty_label="Select User Account",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Employee

        fields = [
            'user',
            'employee_id',
            'phone',
            'department',
            'designation',
            'joining_date',
            'salary'
        ]

        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'salary': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude users who already have an Employee profile, except the one associated with the current instance.
        instance = kwargs.get('instance')
        used_user_ids = list(Employee.objects.exclude(user=None).values_list('user_id', flat=True))
        if instance and instance.user_id:
            if instance.user_id in used_user_ids:
                used_user_ids.remove(instance.user_id)
        
        self.fields['user'].queryset = User.objects.filter(role='EMPLOYEE').exclude(id__in=used_user_ids)