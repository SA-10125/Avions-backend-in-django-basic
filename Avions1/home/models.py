from django.db import models as m

# Create your models here.

class team_member(m.Model):
    name = m.CharField(max_length=100, blank=False, null=False)
    position = m.CharField(max_length=100)
    image = m.CharField(max_length=100000000) #is location of image

    def __str__(self):
        return f"{self.name}-{self.position}"


class gallery_name(m.Model):
    name=m.CharField(max_length=100) #name of image cause readability of database/backend.
    image = m.CharField(max_length=100000000, null=False, blank=False) #is location of image

    def __str__(self):
        return f"{self.name}-{self.image}"