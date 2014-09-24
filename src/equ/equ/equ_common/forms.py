from django import forms

class Article_New(forms.Form):
    name = forms.CharField()
    price = forms.IntegerField(min_value=0)
    description = forms.CharField(widget=forms.Textarea)

# Novcat's development
import os

class UserProfileForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password.widget.attrs = { 'placeholder':'Insert new password' }
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password.widget.attrs = { 'placeholder':'Confirm new password' }
    email = forms.EmailField()
    email.widget.attrs = {'readonly':True}
    mobile = forms.IntegerField(min_value=0)
    state = forms.ChoiceField(choices=(
            ('AL', 'Alabama'),
            ('AK','Alaska'),
            ('AZ','Arizona'),
            ('AR','Arkansas'),
            ('CA','California'),
            ('CO','Colorado'),
            ('CT','Connecticut'),
            ('DE','Delaware'),
            ('DC','District of Columbia'),
            ('FL','Florida'),
            ('GA','Georgia'),
            ('HI','Hawaii'),
            ('ID','Idaho'),
            ('IL','Illinois'),
            ('IN','Indiana'),
            ('IA','Iowa'),
            ('KY','Kentucky'),
            ('LA','Louisiana'),
            ('ME','Maine'),
            ('MD','Maryland'),
            ('MA','Massachusetts'),
            ('MI','Michigan'),
            ('MN','Minnesota'),
            ('MS','Mississippi'),
            ('MO','Missouri'),
            ('MT','Montana'),
            ('NE','Nebraska'),
            ('NV','Nevada'),
            ('NH','New Hampshire'),
            ('NJ','New Jersey'),
            ('NM','New Mexico'),
            ('NY', 'New York'),
            ('NC','North Carolina'),
            ('ND','North Dakota'),
            ('OH','Ohio'),
            ('OK','Oklahoma'),
            ('OR','Oregon'),
            ('PA','Pennsylvania'),
            ('RI','Rhode Island'),
            ('SC', 'South Carolina'),
            ('SD','South Dakota'),
            ('TN','Tennessee'),
            ('TX','Texas'),
            ('UT', 'Utah'),
            ('VT','Vermont'),
            ('VA','Virginia'),
            ('WA','Washington'),
            ('WV','West Virginia'),
            ('WI','Wisconsin'),
            ('WY', 'Wyoming'),
        ), required=False)
    state.widget.attrs = { 'class':'drop', 'style':'width:170px;' }
    city = forms.CharField()
    image = forms.ImageField(required=False)
    image.widget.attrs = { 'class':'add-photo' }
    terms = forms.BooleanField(required=False)

    def clean(self, *args, **kwargs):
        data = super(UserProfileForm, self).clean(*args, **kwargs)
        if 'image' in data and data['image'] != None:
            filename = data['image'].name
            ext = os.path.splitext(filename)[1].lower()
            if ext != '.jpg' and ext != '.png':
                raise forms.ValidationError('Invalid filetype', code='invalid_type')

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    email.widget.attrs = { 'class':'form-control', 'readonly':True }
    password = forms.CharField(widget=forms.PasswordInput)
    password.widget.attrs = { 'class':'form-control' }
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password.widget.attrs = { 'class':'form-control' }

    def clean(self, *args, **kwargs):
        data = super(ForgotPasswordForm, self).clean(*args, **kwargs)
        if 'password' in data and 'confirm_password' in data and data['password'] != str() and data['confirm_password'] != str() and data['password'] != data['confirm_password']:
            raise forms.ValidationError('Passwords do not match', code='incorrect_passwords')