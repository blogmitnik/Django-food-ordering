from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, PrependedAppendedText, FormActions

class EditUserForm(UserChangeForm):
	class Meta:
		model = UserProfile
		fields = ['location', 'gender', 'phone_number', 'birthday', 'photo', 'subscribe']

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']