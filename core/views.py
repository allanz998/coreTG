from django.shortcuts import render, HttpResponse, redirect
import os
from .models import File
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from core.tasks import send_to_channel


def panel(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('file_name')
            desc = request.POST.get('description')
            file = request.FILES.get('file')

            file_name = name.strip()
            description =  desc.strip() 

            try:
                if file_name and file:
                    
                    add_to_db = File(
                        name = file_name,
                        path = file,
                        description = description
                    )
                    add_to_db.save()
                    send_to_channel.delay(add_to_db.pk)
                        
                    return render(request, 'panel.html') 
            except Exception as e: 
                return HttpResponse('File cant be saved. Reason: ' + str(e))
        return render(request, 'panel.html',)
    else:
        return redirect('login') 

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
                user = form.get_user()
                try: 
                    login(request, user)
                except Exception as e:
                   print(e)

                # Check if there is a next parameter in the request
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else: 
                    return redirect('panel')  # Use the name of the home URL pattern if available
        
        else:
            return HttpResponse('Invalid credentials.')
    else:
        return render(request, 'login.html')
    

def logout_view(request):
    request.session.flush()
    return render(request, 'login.html')