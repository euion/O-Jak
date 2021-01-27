from django.shortcuts import render

# Create your views here.
def home(request):
    key = request.session.get('user')
    
    print(type(KeyboardInterrupt))
    print(key)
    
    if key:
        return render(request, 'main.html')
    
    return render(request, 'main.html')