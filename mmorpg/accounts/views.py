import random
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, mail_managers, mail_admins
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=request.POST['email'],
                username=request.POST['username'],
                password=request.POST['password1'],
                is_active=False
            )

            generated_code = Code.objects.create(
                name=User.objects.get(id=user.id),
                code=random.randint(1000, 9999)
            )
            print(generated_code.code)
            send_mail(subject='Confirm your registration.',
                      message=f'Proceed with this confirmation code {generated_code.code} .',
                      from_email=None,
                      recipient_list=[request.POST['email']])
            context = {
                'generated_code': generated_code,
                'user': user
            }
            return render(request, 'reg/confirm.html', context)
        else:
            return render(request, 'reg/reset.html')
    else:
        form = SignUpForm()
        return render(request, 'reg/signup.html', {'form': form})


def confirm(request, code_id):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            user = request.POST['name']
            user_code = request.POST['code']
            confirmation = Code.objects.get(id=code_id)
            if int(user_code) == int(confirmation.code):
                user_upd = User.objects.get(username=confirmation.name)
                user_upd.is_active = True
                user_upd.save()

                mail_managers(
                    subject='New user!',
                    message=f'Hello, manager! New user {user} is registered.'
                )

                mail_admins(
                    subject='News user!',
                    message=f'Hello, admin! New user {user} is registered.'
                )

                return render(request, 'reg/successful.html', {'user': user})
            return render(request, 'reg/unsuccessful.html')
        return render(request, 'regunsuccessful.html')
    else:
        form = ConfirmationForm()
        return render(request, 'reg/confirm.html', {'form': form})


def reset(request):
    obj = User.objects.filter(is_active=False)
    obj.delete()
    return redirect('signup')


class LoginView(FormView):
   model = User
   form_class = LoginForm
   template_name = 'reg/login.html'
   success_url = '/'

   def form_valid(self, form):
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(self.request, username=username, password=password)
      if user is not None:
         login(self.request, user)
      return super().form_valid(form)

