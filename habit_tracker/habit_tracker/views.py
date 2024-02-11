from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render

def logout_view(request):
    logout(request)
    # Redirect to a certain URL after logging out
    return redirect('login')  # Replace 'home' with the name of your desired URL pattern

def login_view(request):
    print(request.POST)

    if request.method == 'POST':
        # Handle form submission
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next', '/habit') # Default to '/' if 'next' is not present
        if next_url == '':
            next_url = '/habit/list'

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)  # Redirect to the 'next' URL after login
        else:
            # Handle invalid login
            pass
    else:
        # Render the login form
        return render(request, 'login.html')