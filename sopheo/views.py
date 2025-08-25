from django.shortcuts import render
from .forms import LearningPathForm
from .models import Module
import serpapi



def generate_learning_map(area, skill_level):
    """Generate learning map for given area and skill level."""
    # Map skill_level to phase
    skill_to_phase = {
        'IDK bro:(': 'Foundations',
        'Kinda Skilled': 'Analysis',
        'I Can Teach You': 'Advanced'
    }
    phase = skill_to_phase.get(skill_level, 'Foundations')  # Default to Foundations
    
    # Check if modules exist for this area and phase
    existing_modules = Module.objects.filter(phase=phase, topic__icontains=area)
    
    if existing_modules.exists():
        return existing_modules.order_by('sequence')
    
    else:
        client = serpapi.Client(api_key="75c7c3e1c56f4719c493f2ef5d91c4959cf4c5ec93d5bb13113f85d7731bbb9b")

        # Parameters go in a dictionary
        params = {
            'engine': 'google',
            'q': 'how to learn {area} {skill_level}',
            'location': 'United States',
            'hl': 'en',
            'gl': 'us',
        }

        try:
            result = client.search(params)
            results = json.loads(result).get('organic_results', []) if isinstance(result, str) else result.get('organic_results', [])
        except Exception as e:
            print(f"SerpAPI error: {e}")
            return Module.objects.none()
            
        # Create new modules
        for i, result in enumerate(results, 1):
            Module.objects.create(
                phase=phase,
                topic=result.get('title', 'Untitled'),
                description=result.get('snippet', 'No description available'),
                sequence=i
            )
        return Module.objects.filter(phase=phase, topic__icontains=area).order_by('sequence')

def start(request):
    form = LearningPathForm(request.POST or None)
    lrning_map = None
    if request.method == 'POST' and form.is_valid():
        area = form.cleaned_data['area'].lower()
        skill_level = form.cleaned_data['skill_level']
        lrning_map = generate_learning_map(area, skill_level)[:3]  # Limit to 3 modules
    return render(request, 'sopheo/start.html', {'form': form, 'lrning_map': lrning_map})

def full_map(request):
    area = request.GET.get('area', '').lower()
    skill_level = request.GET.get('skill_level', '')
    lrning_map = None
    if area and skill_level:
        lrning_map = generate_learning_map(area, skill_level)  # Full map
    return render(request, 'sopheo/full_map.html', {'lrning_map': lrning_map, 'area': area, 'skill_level': skill_level})