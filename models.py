from django.db import models
from django.contrib.auth.models import User, AbstractUser

#newly added code 
#class Account(AbstractUser):
    #is_student = models.BooleanField(default=False)
    #is_teacher = models.BooleanField(default=False)

#end of new code

class Course1(models.Model):
    title = models.CharField(max_length=500)
    files =  models.FileField(upload_to='multipleuser/files', null=True, verbose_name="")
    created = models.DateTimeField(auto_now_add=True)
    #foreign key takes the id of the user(here instructor) assign it with the course created by him/her
    #one instructor can have a lots of different courses (one to many), but one course belong to one particular instructor (one to one)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        #to view the videos uploaded by instructor
        return self.title + ": " + str(self.files)

