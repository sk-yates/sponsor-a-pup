from django import forms

class SignupNameForm(forms.Form):
    TITLE_CHOICES = [
        ('Mr', 'Mr.'),
        ('Ms', 'Ms.'),
        ('Mrs', 'Mrs.'),
        ('Dr', 'Dr.'),
        ('Miss', 'Miss.'),
        ('Prof', 'Prof'),
        ('Rev', 'Rev.'),
        ('Mx', 'Mx.'),
    ]
    
    title = forms.ChoiceField(
        choices=TITLE_CHOICES, required=True, label="Title",
        widget=forms.Select(attrs={'class': 'form-dropdown'})
    )
    first_name = forms.CharField(
        max_length=50, required=True, label="First Name",
        widget=forms.TextInput(attrs={'placeholder': 'Type here...', 'class': 'form-input'})
    )
    last_name = forms.CharField(
        max_length=50, required=True, label="Last Name",
        widget=forms.TextInput(attrs={'placeholder': 'Type here...', 'class': 'form-input'})
    )