from django.shortcuts import render
def home(request):
    return render(request, 'catalog/home.html')
def contacts(request):
    success = False
    if request.method == 'POST':
        success = True
    return render(request, 'catalog/contacts.html', {'success': success})
