from django import forms
from .models import Leave


class LeaveForm(forms.ModelForm):

    class Meta:

        model = Leave

        fields = [

            "leave_type",

            "start_date",

            "end_date",

            "reason",

        ]

        widgets = {

            "start_date":

            forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "end_date":

            forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "reason":

            forms.Textarea(
                attrs={
                    "rows": 4
                }
            ),

        }