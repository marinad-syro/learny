from django import forms

class LearningPathForm(forms.Form):
    area = forms.CharField(max_length=200, label="Choose an area to explore")
    daily_time = forms.ChoiceField(choices=[('2', '2 minutes/day'), ('5', '5 minutes/day'), ('10', '10 or more minutes/day')]) 
    