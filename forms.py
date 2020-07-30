from django.forms import ModelForm
from .models import Course1

class CreateCourseForm(ModelForm):
    class Meta:
        model = Course1
        fields = [ 'title' , 'files']