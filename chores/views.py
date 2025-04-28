from django.shortcuts import render
# Create your views here.
def chores(request):
    return render(request, 'chores/chores.html')