from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=50)
    password = forms.CharField(label="password", max_length=50)
    #email    = forms.CharField(label="email", max_length=50)
    #checkbox = forms.BooleanField(label="Remember", required=False)

class RegisterForm(forms.Form):
    username = forms.CharField(label="username", max_length=50)
    password = forms.CharField(label="password", max_length=50)
    passwordCheck = forms.CharField(label="passwordCheck", max_length=50)
    email    = forms.CharField(label="email", max_length=50)

class SettingsForm(forms.Form):
    username = forms.CharField(label="username", max_length=50)
    password = forms.CharField(label="password", max_length=50)
    email    = forms.CharField(label="email", max_length=50)

class EditForm(forms.Form):
    title = forms.CharField(label="title", max_length=100, required=True)
    slug  = forms.CharField(label="slug", max_length=100, required=True)
    body  = forms.CharField(widget=forms.Textarea, required=True)

class ModifyWordForm(forms.Form):
    word      = forms.CharField(label="word", max_length=100, required=True)
    e_meaning = forms.CharField(label="e_meaning", max_length=100, required=False)
    c_meaning = forms.CharField(label="c_meaning", max_length=100, required=False)
    source    = forms.CharField(label="source",widget=forms.Textarea,required=False)
    helper    = forms.CharField(label="helper", max_length=100, required=False)
    
class ModifyEtymaForm(forms.Form):
    root    = forms.CharField(label="root", max_length=100, required=True)
    meaning = forms.CharField(label="meaning", max_length=100, required=True)
    words   = forms.CharField(label="words", max_length=1000, required=False)
    function= forms.CharField(label="function", max_length=200, required=False)
    origin  = forms.CharField(label="origin", max_length=100, required=False)
