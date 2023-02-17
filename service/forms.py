import datetime

from django.contrib.auth.models import User
from django.forms import ModelForm, ModelChoiceField, TextInput, DateTimeInput, Select, DateTimeField

from service.models import Mailing, MailingSettings


class MailingForm(ModelForm):

    class Meta:
        model = Mailing
        fields = ('title', 'body')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(MailingForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(MailingForm, self).clean()
        body = cleaned_data.get("body")
        if not body:
            msg = "Please, enter body content"
            self.add_error('body', msg)


class MailingSettingsForm(ModelForm):

    send_in = DateTimeField(required=False, widget=DateTimeInput(attrs={'type': 'datetime-local'}),
                            localize=True, input_formats=['%Y-%m-%dT%H:%M'])

    def __init__(self, users, *args, **kwargs):
        super(MailingSettingsForm, self).__init__(*args, **kwargs)
        self.fields['send_to'].queryset = users

    class Meta:
        model = MailingSettings
        exclude = ('mailing', )
