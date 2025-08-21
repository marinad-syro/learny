from django.db import models

class Module(models.Model):
    phase = models.CharField(max_length=50)  # e.g., "Foundations"
    sequence = models.IntegerField()  # Order in phase
    topic = models.CharField(max_length=200)  # e.g., "What is Investing?"
    description = models.TextField() #briefly talk abt the module
    def __str__(self):
        total_in_phase = Module.objects.filter(phase=self.phase).count()
        return f"{self.phase}, {self.sequence}/{total_in_phase}: {self.topic}"
        #this counts the total modules in a phase, gives you the phase, the sequence (eg. 2/5), and the module name