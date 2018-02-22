from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import re
import os

sex_choices = (('F', 'Female'),
				('M', 'Male'),
				('S', 'Secret'))

def validate_nickname(nickname):
	pattern = re.compile(r'^[a-zA-Z]+[a-zA-Z0-9]*$')
	if re.match(pattern, nickname):
		return True
	else:
		return False

def upload_to(instance, filename):
	return os.path.join(str(instance.id), filename)

class User(AbstractUser):
	sex = models.CharField(choices=sex_choices, max_length=10, default='S')
	nickname = models.CharField(max_length=10, validators=((validate_nickname,)))
	age = models.PositiveIntegerField(default=17)
	mood = models.TextField(blank=True)
	introduction = models.TextField(blank=True)
	photo = models.ImageField(upload_to=upload_to, default='dragonCat.jpg')
	follows = models.TextField(blank=True, default='')

	class Meta(AbstractUser.Meta):
		pass


class Blog(models.Model):
	content = models.TextField(blank=True)
	update_time = models.DateTimeField(auto_now=True)
	followers = models.TextField(blank=True)
	followers_amt = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def can_be_followed_by(self, user_id):
		return not int(user_id) in (int(x) for x in self.followers.split(';') if x != '') and int(user_id) != self.user.id


class Comment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField(blank=True)
	reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
	blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
	create_time = models.DateTimeField(auto_now=True)
	my_floor = models.PositiveIntegerField(default=1)



