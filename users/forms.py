# users/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Speciality, Message

class CustomUserCreationForm(UserCreationForm):
    """
    Extends the native Django UserCreationForm to explicitly capture 
    essential farmer profile details during account initialization.
    """
    """
    Subclasses Django's UserCreationForm to explicitly append CSS styling hooks 
    and custom display attributes to all field elements during creation.
    """

    class Meta:
        model = User # Use the built-in User model for authentication and basic user data
        # Re-arrange ordering: capture structural baseline contact data first
        # fields = ['first_name', 'email', 'username', 'password1', 'password2']
        fields = ['first_name', 'email', 'username']        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Override structural form labels for cleaner presentation fields
        self.fields['first_name'].label = "Full Name"
        self.fields['first_name'].required = True
        self.fields['email'].required = True

        # Programmatic Styling Loop: 
        # Inject modern form classes to every field widget
        for name, field in self.fields.items():
            #field.widget.attrs.update({'class': 'input input--text'})
            field.widget.attrs.update({'class': 'input input--text'}) 

class ProfileForm(forms.ModelForm):
    """
    Form for editing user profile information, including both User and Profile model fields.
    """
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'county', 'bio', 'profile_image', 
                  'whatsapp_link', 'website', 'social_twitter', 'youtube']
        #fields = '__all__' # <--- Alternative to explicitly listing fields, but less secure if new fields are added to the model in the future without updating the form. Use with caution.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Programmatic Styling Loop: 
        # Inject modern form classes to every field widget
        for name, field in self.fields.items():
            #field.widget.attrs.update({'class': 'input input--text'})
            field.widget.attrs.update({'class': 'input input--text'})         

class SpecialityForm(forms.ModelForm):
    # 1. Change to a simple ChoiceField (empty by default, populated dynamically below)
    name = forms.ChoiceField(
        choices=[], 
        label="Speciality Name",
        required=True
    )

    class Meta:
        model = Speciality
        fields = ['name', 'description']
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 2. Extract only UNIQUE, non-empty names from your existing database records
        unique_db_names = Speciality.objects.values_list('name', flat=True).distinct()
        
        # 3. Build a clean dropdown choice list format: (database_value, display_text)
        dynamic_choices = [('', 'Select a Speciality...')]
        for choice_name in unique_db_names:
            if choice_name and choice_name.strip():  # Safely ignore empty or None data rows
                dynamic_choices.append((choice_name.strip(), choice_name.strip()))
                
        # 4. Inject the unique choices list straight into the field widget
        self.fields['name'].choices = dynamic_choices

        # 5. Your premium style classes loop injection stays perfect
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Programmatic Styling Loop: 
        # Inject modern form classes to every field widget
        for name, field in self.fields.items():
            #field.widget.attrs.update({'class': 'input input--text'})
            field.widget.attrs.update({'class': 'input'})                      
