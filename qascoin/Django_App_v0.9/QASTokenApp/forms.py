from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, login, logout, password_validation
from .models import Registration
from django.core.exceptions import ValidationError
from django.core import validators
from django.core.validators import RegexValidator

User = get_user_model()

class SignUpForm(UserCreationForm):
    def check_size(value):
      if len(value) < 8:
          raise forms.ValidationError("password is too short, please input at least 8 character")

    username = forms.CharField()
    email = forms.CharField(max_length=30, required=True, validators=[RegexValidator('^[A-Za-z0-9._%+-]+@ey.com$', message=("Must have a valid ey email address"), )])
    password1 = forms.CharField(widget = forms.PasswordInput, validators = [check_size, ])
    password2 = forms.CharField(help_text = 'Confirm your password', widget = forms.PasswordInput, required = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'form__input', 
            'required':'this field is required', 
            'invalid': 'Enter a valid value',
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'Username', 
            'maxlength': '16', 
            'minlength': '4', 
            })

        self.fields['email'].widget.attrs.update({ 
            'class': 'form__input', 
            'required':'this field is required', 
            'invalid': 'Enter a valid value',
            'name':'email', 
            'id':'email', 
            'type':'text', 
            'placeholder':'Email', 
            })

        self.fields['password1'].widget.attrs.update({ 
            'class': 'form__input', 
            'required':'this field is required', 
            'invalid': 'Enter a valid value',
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'Password', 
            'maxlength': '22', 
            'minlength': '8', 
            })

        self.fields['password2'].widget.attrs.update({ 
            'class': 'form__input', 
            'required':'this field is required', 
            'invalid': 'Enter a valid value',
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'Confirm Password', 
            'maxlength': '22', 
            'minlength': '8', 
            })

        def clean(self):
            cleaned_data = super(UserForm, self).clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                raise forms.ValidationError(
                    "password and confirm_password does not match"
                )
'''
class SignUpForm(UserCreationForm):
    error_messages = {
        "password_mismatch": "The two password fields didn’t match.",
    }
    password1 = forms.CharField(
        label= "Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label= "Password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text= "Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs.update({ 
            'class': 'form__input', 
            'required':'this field is required', 
            'invalid': 'Enter a valid value',
            'name':'username', 
            'id':'username', 
            'type':'text', 
            'placeholder':'Username', 
            'maxlength': '16', 
            'minlength': '4', 
            })

        self.fields['password1'].widget.attrs.update({ 
            'class': 'form__input', 
            'required':'this field is required', 
            'invalid': 'Enter a valid value',
            'name':'password1', 
            'id':'password1', 
            'type':'password', 
            'placeholder':'Password', 
            'maxlength': '22', 
            'minlength': '8', 
            })

        self.fields['password2'].widget.attrs.update({ 
            'class': 'form__input', 
            'required':'this field is required', 
            'invalid': 'Enter a valid value',
            'name':'password2', 
            'id':'password2', 
            'type':'password', 
            'placeholder':'Confirm Password', 
            'maxlength': '22', 
            'minlength': '8', 
            })

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
'''

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username = username, password = password)
        if not user or not user.is_active:
            raise forms.ValidationError("Incorrect username/password combination")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['email']