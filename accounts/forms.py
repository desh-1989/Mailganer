from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, PasswordInput, Select, ChoiceField, DateField, \
    DateInput, ValidationError


class LoginForm(ModelForm):
    double_pass = CharField(widget=PasswordInput(), label='Password again')
    birthday = DateField(widget=DateInput(attrs={'type': 'date'}), label='Birthday')
    state = ChoiceField(
        label='Select your status',
        choices=(
            ('o', 'owner'),
            ('s', 'respondent')
        ),
        widget=Select(attrs={'class': 'select-status'})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'birthday',
                  'email', 'password', 'double_pass', 'state']
        widgets = {
            'password': PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        password_main = cleaned_data.get("password")
        password_double = cleaned_data.get("double_pass")

        if password_main != password_double:
            msg = "passwords don't match"
            self.add_error('password', msg)
            self.add_error('double_pass', msg)