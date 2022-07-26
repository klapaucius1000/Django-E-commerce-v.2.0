import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
	"""Creating SuperUser, Staff  and User model"""

	def create_superuser(self, email, name, password, **other_fields):
		other_fields.setdefault('is_staff', True)
		other_fields.setdefault('is_superuser', True)
		other_fields.setdefault('is_active', True)

		if other_fields.get('is_staff') is not True:
			raise ValueError(
				'SuperUser must be assigned to is_staff = True.'
			)
		if other_fields.get('is_superuser') is not True:
			raise ValueError(
				'SuperUser must be assigned to is_superuser = True.'
			)
		if other_fields.get('is_active') is not True:
			raise ValueError(
				'SuperUser must be assigned to is_active = True.'
			)

		return self.create_user(email, name, password, **other_fields)

	def create_user(self, email, name, password, **other_fields):

		if not email:
			raise ValueError(_('You must provide an email address'))

		email = self.normalize_email(email)
		user = self.model(email=email, name=name, **other_fields)
		user.set_password(password)
		user.save()
		return user


class Customer(AbstractBaseUser, PermissionsMixin):
	"""Creating Customer model"""

	name = models.CharField(max_length=150)
	email = models.EmailField(_('email address'), unique=True)
	mobile = models.CharField('Its completely optional', max_length=20, unique=True)
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	objects = CustomAccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	class Meta:
		verbose_name = "Accounts"
		verbose_name_plural = "Accounts"

	def email_user(self, subject, message):
		send_mail(
			subject,
			message,
			'l@1.com',
			[self.email],
			fail_silently=False,
		)

	def __str__(self):
		return self.name


class Address(models.Model):
	"""Creating delivery adress model. With UUID"""

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	customer = models.ForeignKey(Customer, verbose_name=_("Customer"), on_delete=models.CASCADE)
	full_name = models.CharField(_("Full Name"), max_length=150)
	phone_number = models.CharField(max_length=15, blank=True)
	zipcode = models.CharField(max_length=12, blank=True)
	address_line_1 = models.CharField(max_length=150, blank=True)
	address_line_2 = models.CharField(max_length=150, blank=True)
	city = models.CharField(max_length=150, blank=True)
	delivery_instructions = models.CharField(_("Delivery instructions"), max_length=255)
	created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
	updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
	default = models.BooleanField(_("Default"), default=False)



	class Meta:
		verbose_name = "Address"
		verbose_name_plural = "Addresses"

	def __str__(self):
		return "{}Address".format(self.full_name)
