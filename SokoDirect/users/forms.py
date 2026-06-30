from django import forms
from django.contrib.auth.models import User


ROLE_CHOICES = [
    ('', 'Select Role'),
    ('buyer', 'Buyer'),
    ('farmer', 'Farmer'),
]


class RegisterForm(forms.ModelForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address'
            }
        )
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select,
        label=''
    )

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )

    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password'
            }
        )
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email'
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Username'
                }
            )
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = None

    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():

            raise forms.ValidationError(
                'Account already exists.'
            )

        return email

    def clean(self):

        cleaned_data = super().clean()

        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 and p2 and p1 != p2:

            raise forms.ValidationError(
                'Passwords do not match'
            )

        return cleaned_data

    def save(self, commit=True):

        user = super().save(commit=False)

        user.email = self.cleaned_data['email']

        user.set_password(
            self.cleaned_data['password1']
        )

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):

    identifier = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username / Email'
            }
        )
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )