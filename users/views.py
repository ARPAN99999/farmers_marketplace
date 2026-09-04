from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .forms import RegistrationForm

def register(request):
	form = RegistrationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
		from .models import Profile
		Profile.objects.create(user=user, role=form.cleaned_data['role'], phone=form.cleaned_data['phone'], location=form.cleaned_data['location'])
		login(request, user)
		return redirect('products:list')
	return render(request, 'users/register.html', {'form': form})

def login_view(request):
	form = AuthenticationForm(request, data=request.POST or None)
	if request.method == 'POST' and form.is_valid():
		login(request, form.get_user())
		return redirect('products:list')
	return render(request, 'users/login.html', {'form': form})
