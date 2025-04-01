from django import forms
from .models import Customer, Interaction
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'company', 'status', 'notes']
        widgets = {
            'notes':forms.Textarea(attrs={'rows':3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
            'phone',
            'company',
            'status',
            'notes',
            Submit('submit', 'Save Customer', css_class='btn btn-primary mt-3')
        )


class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ['interaction_type', 'subject', 'notes', 'date']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'interaction_type',
            'subject',
            'notes',
            'date',
            Submit('submit', 'Save Interaction', css_class='btn btn-primary mt-3')
        )

for form in [CustomerForm, InteractionForm]:
    for field_name, field in form.base_fields.items():
        field.widget.attrs['class'] = 'form-control'