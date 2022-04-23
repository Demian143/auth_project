from django import forms


class SignInForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(label="email")
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput)


class LoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


class DeleteAccountForm(forms.Form):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        max_length=100, widget=forms.PasswordInput)
