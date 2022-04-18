from django import forms


class SignInForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(label="email")
    password = forms.CharField(label="password",
                               max_length=20,
                               widget=forms.PasswordInput)
