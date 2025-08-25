from django import forms

class LearningPathForm(forms.Form):
    area = forms.CharField(max_length=200, label="Choose an area to explore")
    skill_level = forms.ChoiceField(choices=[('beginner', 'IDK bro:('), ('intermediate', 'Kinda Skilled'), ('advanced', 'I Can Teach You')]) 
