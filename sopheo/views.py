from django.shortcuts import render
from .forms import LearningPathForm

def start(request):
    form = LearningPathForm()
    return render(request, 'sopheo/start.html', {'form': form})
    



