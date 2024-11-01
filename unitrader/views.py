from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def home(request):
    return render(request, "unitrader/home.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Check if username is empty
        if not username:
            messages.error(request, "Username cannot be empty")
            return render(request, "unitrader/signup.html")
            
        # Check if first name or last name is empty
        if not first_name or not last_name:
            messages.error(request, "First name and last name cannot be empty")
            return render(request, "unitrader/signup.html")
            
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "unitrader/signup.html")
            
        # Check if passwords are empty
        if not password1 or not password2:
            messages.error(request, "Password fields cannot be empty")
            return render(request, "unitrader/signup.html")
            
        # Check password length
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return render(request, "unitrader/signup.html")
    
        if password1 == password2:
            # Check password complexity
            if not any(char.isdigit() for char in password1):
                messages.error(request, "Password must contain at least one number")
                return render(request, "unitrader/signup.html")
                
            if not any(char.isupper() for char in password1):
                messages.error(request, "Password must contain at least one uppercase letter")
                return render(request, "unitrader/signup.html")
                
            user = User.objects.create_user(
                username=username,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('signin')
        else:
            messages.error(request, "Passwords do not match")   
    return render(request, "unitrader/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('signin')

    return render(request, "unitrader/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('home')