from django import forms

from django.core.exceptions import ValidationError


class AddPost(forms.Form):
    post_text = forms.CharField(max_length=1000, min_length=1)

    def clean_post_text(self):
        text = self.cleaned_data['post_text']
        return text


class AddForum(forms.Form):
    title = forms.CharField(max_length=100, min_length=1)
    group = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        groups = kwargs.pop('groups')
        super(AddForum, self).__init__(*args, **kwargs)
        self.fields['group'].choices = groups

    def clean_post_text(self):
        title = self.cleaned_data['title']
        return title


class AddThread(forms.Form):
    title = forms.CharField(max_length=100, min_length=1)

    def clean_post_text(self):
        title = self.cleaned_data['title']
        return title


class AddUser(forms.Form):
    login = forms.CharField(max_length=20, min_length=1)        #jakoś by tu uniqa wcisnąć
    password = forms.CharField(widget=forms.PasswordInput)
