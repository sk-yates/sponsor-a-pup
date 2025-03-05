from django import forms

class SignupNameForm(forms.Form):
    TITLE_CHOICES = [
        ('Mr', 'Mr.'),
        ('Ms', 'Ms.'),
        ('Mrs', 'Mrs.'),
        ('Dr', 'Dr.'),
        # Add more options as needed
    ]
    
    title = forms.ChoiceField(choices=TITLE_CHOICES, required=True, label="Title")
    first_name = forms.CharField(max_length=50, required=True, label="First Name")
    last_name = forms.CharField(max_length=50, required=True, label="Last Name")