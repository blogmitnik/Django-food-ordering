from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

@login_required()
def editProfileView(request):
	if request.user.is_authenticated:
		user_form = UserForm(instance=request.user)
		ProfileFormSet = inlineformset_factory(User, UserProfile, can_delete=False, fields=('location', 'gender', 'phone_number', 'birthday', 'subscribe', 'photo'))
		if request.method == 'POST':
			user = User.objects.get(pk=request.user.id)
			user_form = UserForm(request.POST, request.FILES, instance=user)
			formset = ProfileFormSet(request.POST, request.FILES, instance=user)
			if user_form.is_valid():
				created_user = user_form.save()
				if formset.is_valid():
					created_user.save()
					formset.save()
					messages.success(request, f'Your profile has been updated!')
					return redirect('user:edit_profile')
		else:
			formset = ProfileFormSet(instance=request.user)
		return render(request, 'edit_user.html', {'formset': formset, 'user_form': user_form})
	else:
		raise PermissionDenied

@login_required()
def change_password(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			password_form = PasswordChangeForm(request.user, request.POST)
			if password_form.is_valid():
				user = password_form.save()
				update_session_auth_hash(request, user)
				messages.success(request, 'Your password was successfully updated!')
				return redirect('user:change_password')
			else:
				messages.error(request, 'Please correct the error below!')
		else:
			password_form = PasswordChangeForm(request.user)
		return render(request, 'change_password.html', {'password_form': password_form})
	else:
		raise PermissionDenied
