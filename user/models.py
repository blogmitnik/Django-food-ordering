from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from shop.models import Place

class PlaceCategory(models.Model):
	name = models.CharField(max_length=30)
	parent = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.name

class UserProfile(User):
	GENDER_SELECTION = (
		(0, 'Male'), 
		(1, 'Female'),
	)
	OFFICE_SELECTION =(
		(1, 'QRDC (Taipei)'), 
		(2, 'CSMC (Factory A)'), 
		(3, 'CSMC (Factory C)'), 
		(4, 'CSMC (Factory D)'),
		(5, 'QSMC (F4)'), 
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE, parent_link=True)
	gender = models.PositiveSmallIntegerField(choices=GENDER_SELECTION, default=0)
	location = models.ForeignKey(PlaceCategory, on_delete=models.CASCADE)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+8860806449'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
	can_order = models.BooleanField(default=True)
	subscribe = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	photo = models.ImageField(upload_to='profile_pucture', max_length=255, blank=True, default='profile-default.jpg')
	birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)

	class Meta(User.Meta):
		db_table = 'UserInfo'

	def __str__(self):
		return str(self.id)