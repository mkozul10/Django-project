from django.db import models
from django.db.models.signals import pre_save,post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver
from django.core.files.storage import default_storage
import os

# Create your models here.
def upload_location(instance,filename):
    base_path='blog'
    author_id=str(instance.author.id)
    title=str(instance.title)
    file_path=os.path.join(base_path,author_id,title,filename)
    return default_storage.path(file_path)


class BlogPost(models.Model):
    title=              models.CharField(max_length=50,null=False,blank=False)
    body=               models.TextField(max_length=5000,null=False,blank=False)
    image=              models.ImageField(upload_to=upload_location,null=False,blank=False)
    date_published=     models.DateTimeField(auto_now_add=True,verbose_name="date published")
    date_updated=       models.DateTimeField(auto_now=True,verbose_name="date updated")
    author=             models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    slug=               models.SlugField(max_length=200,blank=True,unique=True)

    def __str__(self):
        return self.title


@receiver(post_delete,sender=BlogPost)
def submission_delete(sender,instance,**kwargs):
    instance.image.delete(False)
    
@receiver(pre_save, sender=BlogPost)
def pre_save_blog_post_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=slugify(instance.author.username+"-"+instance.title)
    pre_save.connect(pre_save_blog_post_receiver,sender=BlogPost)   


