from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import UserProfile, PlaceCategory
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field, Fieldset, ButtonHolder
from crispy_forms.bootstrap import AppendedText, PrependedText, PrependedAppendedText, FormActions
from user.fields import GroupedModelChoiceField
from .widgets import CountableWidget
from crispy_forms.helper import FormHelper

class SignUpForm(UserCreationForm):
	GENDER_SELECTION = (
		(0, 'Male'), 
		(1, 'Female'),
	)
	first_name = forms.CharField(max_length=100, required=True)
	last_name = forms.CharField(max_length=100, required=True)
	email = forms.EmailField(max_length=250, required=True)
	phone_number = forms.CharField(max_length=17, required=False, help_text='Digits and \'+\' only.')
	gender = forms.ChoiceField(choices=GENDER_SELECTION)
	location = GroupedModelChoiceField(
		queryset=PlaceCategory.objects.exclude(parent=None), 
		choices_groupby='parent',
		label='Office place',
		initial = ''
	)
	#subscribe = forms.BooleanField(required=True, widget=widgets.ToggleWidget(options={ 'on': 'Subscribe', 'off': 'Nope', 'onstyle':'info', 'offstyle':'danger', 'required':True }))

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)
		self.fields['phone_number'].widget.attrs.update({'placeholder':'ex: +8860806449'})
		self.fields['birthday'].widget.attrs.update({'placeholder':'YYYY-MM-DD'})
		#self.fields['photo'].widget.attrs.update({'class':'btn btn-outline-info btn-lg', 'required': False})
		self.fields['subscribe'].widget.attrs.update({'data-toggle':'toggle', 'class':'toggle-subscribe', 'data-on': 'Yep', 'data-off': 'Nope', 'data-onstyle':'info', 'data-offstyle':'light', 'required':True})
		self.fields['subscribe'].label = ''
		self.fields['subscribe'].help_text = 'Subscribe to our newsletter?'

	class Meta:
		model = UserProfile
		fields = ['username', 'first_name', 'last_name', 'email', 'location', 'gender', 'phone_number', 'birthday', 'subscribe', 'photo']

class CountableMessageForm(forms.Form):
	memo = forms.CharField(label="Order notes", widget=forms.Textarea(attrs={"rows":10, "cols":40}))

	def __init__(self, *args, **kwargs):
		super(CountableMessageForm, self).__init__(*args, **kwargs)
		self.fields['memo'].widget = CountableWidget(attrs={'data-max-count': 100, 'data-count': 'characters', 'data-count-direction':'down'})
		self.fields['memo'].widget.attrs.update({'placeholder':'Leave your notes here...'})
		self.fields['memo'].help_text = "Type up to 100 characters"
		self.fields['memo'].label = ""

		self.helper = FormHelper()
		self.helper.help_text_inline = False
