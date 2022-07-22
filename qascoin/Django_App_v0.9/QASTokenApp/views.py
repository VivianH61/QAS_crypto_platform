from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode
from .forms import SignUpForm, UserLoginForm, RegistrationForm
from django.contrib.auth import authenticate, get_user_model, login, logout
from .fund import generate_key_pair
from json import dumps
from .models import Registration
from django.contrib.sites.shortcuts import get_current_site
import random
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
import six
from django.contrib import messages

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
				six.text_type(user.pk) + six.text_type(timestamp)
			)

account_activation_token = AccountActivationTokenGenerator()

'''
def RegistrationView(request):
	form = RegistrationForm()
	if request.method == 'POST':
		email = request.POST.get('email')
		user = Registration(email=email)
		domain_name = get_current_site(request).domain
		token = str(random.random()).split('.')[1]
		user.token = token
		link = f'http://{domain_name}/QASTokenApp/verify/{token}'
		send_mail(
			'Email Verification',
			f'Please click {link} to verify your email',
			settings.EMAIL_HOST_USER,
			[email],
			fail_silently=False,
		)
		return HttpResponse('The mail has been sent!')
	return render(request, 'registration/register.html', {'form': form})
'''

def activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return redirect('home')
	else:
		return HttpResponse('account activation incorrect!')

'''
def verify(request, token):
	try:
		user = Registration.objects.filter(token = token)
		print(user.token)
		if user:
			user.is_verified = True
		return render(request, 'signup.html')
	except Exception as e:
		return redirect('signup')
'''

def login_view(request):
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if request.POST and form.is_valid():
		user = form.login(request)
		if user:
			login(request, user)
			return redirect("home")
	return render(request, "registration/login.html", {"form":form, "title":title})

def SignUpView(request):

	if request.user.is_anonymous:
		form = SignUpForm(request.POST or None)
		if request.POST:
			if form.is_valid():
				user = form.save(commit=False)
				user.is_active = False
				user.save()

				email = request.POST.get('email')
				domain_name = get_current_site(request).domain
				token = account_activation_token.make_token(user)
				uid = urlsafe_base64_encode(force_bytes(user.pk))
				link = f'http://{domain_name}/QASTokenApp/activate/{uid}/{token}'
				send_mail(
					'Email Verification',
					f'Please click {link} to verify your email',
					settings.EMAIL_HOST_USER,
					[email],
					fail_silently=False,
				)
				return HttpResponse('An confirmation email has been sent to your email address!')
			else:
				messages.info(request, 'invalid registration details')

		return render(request, "registration/signup.html", {'form': form})
	else:
		return redirect("home")

	'''
	if request.user.is_anonymous:
		form = SignUpForm(request.POST or None)
		if request.POST and form.is_valid():
			username = form.cleaned_data.get("username")
			password = form.cleaned_data.get("password1")
			form.clean_password2()
			form.save()
			new_user = authenticate(username=username, password=password)
			if new_user is not None:
				login(request, new_user)
				return redirect("home")
	else:
		return redirect("home")
	form = SignUpForm()
	context = {
		"form": form
	}
	return render(request, "registration/signup.html", context)
	'''

def real_home(request):
	return render(request, "real_home.html")

def ICOView(request):
	return render(request, 'index.html')

def private_key(request):
	return render(request, 'account.html')

def handle_private_key(request):
	try:
		[private, public] = generate_key_pair()
		context = {
	    'public': public,
	    'private': private
		}
		dataJSON = dumps(context)
		print("handled")
		return render(request, "account.html",  {'data': dataJSON})
	except:
		print("please wait a second")
		context = {
	    'public': 'please wait a second and try again',
	    'private': 'please wait a second and try again'
		}
		dataJSON = dumps(context)
		return render(request, "account.html",  {'data': dataJSON})