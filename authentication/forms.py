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


class UpdatePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(widget=forms.PasswordInput)


class UpdateUserNameForm(forms.Form):
    new_username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UpdateEmailForm(forms.Form):
    new_email = forms.EmailField()
    confirm_new_email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
