from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth

# Create your views here.
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse(
                {'username_error': 'username should only contain alphanumeric characters'},
                status = 400
            )
        return JsonResponse({'username_valid': True})

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse(
                {'email_error': 'email is invalid'},
                status = 400
            )
            
        if User.objects.filter(email = email).exists():
            return JsonResponse(
                {'email_error': 'this email is already registered'},
                status = 409
            )

        return JsonResponse({'email_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'accounts/register.html')
    
    def post(self, request):

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(email = email).exists():
            if len(password) < 6:
                messages.error(request, 'Password too short')
                return render(request, 'accounts/register.html', context)
            

            user = User.objects.create_user(username = username, email = email)
            user.set_password(password)
            user.is_active = False
            user.save()
            
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            domain = get_current_site(request).domain
            link = reverse('activate', kwargs = {'uidb64': uidb64, 'token': token_generator.make_token(user)})
            activate_url = 'http://' + domain + link

            email_subject = 'Activate your account for iSpend'
            email_body = "Hi, ' + user.username + '! Let's use the following link to verify your account:\n" + activate_url
            email_msg = EmailMessage(
                email_subject,
                email_body,
                "noreply@ispend.com",
                [email],
            )
            email_msg.send(fail_silently = False)
            messages.success(request, 'Account successfully created. Check your email to activate your account')
        else:
            messages.error(request, 'Provided email address is already in use')

        return render(request, 'accounts/register.html')
    
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = id)
        except Exception:
            messages.error(request, 'Invalid activation link')
        else:
            if token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Account successfully activated')
            else:
                messages.warning(request, 'User already activated')
     
        finally:
            return redirect('login')

class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        print(email + ":" + password)

        if email and password:
            user = authenticate_user(email, password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username)
                    return redirect('expenses')
                messages.error(request, 'Please check your email to activate your account')
                return render(request, 'accounts/login.html')
            
            messages.error(request, 'Invalid email/password. Please try again.')
            return render(request, 'accounts/login.html')
        
        messages.warning(request, "Required field(s) not provided")
        return render(request, 'accounts/login.html')
    
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        messages.success(request, 'You have logged out')
        return redirect('login')

# helper functions
def authenticate_user(email, password):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
    return None