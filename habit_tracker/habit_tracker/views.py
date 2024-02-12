from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render

#TODO: move them to their own account app inside this project
def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    print(request.POST)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST.get('next', '/habit')
        if next_url == '':
            next_url = '/habit/list'

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')