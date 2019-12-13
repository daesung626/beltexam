from django.db import models
import re  # regex
from django.contrib import messages
from django.contrib.messages import get_messages

# Create your models here.

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+$')
# Need this for emails / Import this


class UserManager(models.Manager):
    def is_reg_valid(self, request):
        if len(request.POST['first_name']) < 1:
            messages.error(
                request, 'First name must be more than 1 characters!')

        if len(request.POST['last_name']) < 1:
            messages.error(
                request, 'Last name must be more than 1 characters!')

        if not EMAIL_REGEX.match(request.POST['email']):
            messages.error(request, 'Email must be the correct format!')

        if len(request.POST['password']) < 1:
            messages.error(request, 'Password must be at least 1 characters!')

        if request.POST['password'] != request.POST['password_confirm']:
            messages.error(request, 'Passwords must match!')

        error_messages = messages.get_messages(request)
        # don't clear messages due to them being accessed
        error_messages.used = False
        return len(error_messages) == 0


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()  # Make sure you add this
    # wishes


class WishManager(models.Manager):
    def is_form_valid(self, request):
        if len(request.POST['item_name']) < 3:
            messages.error(request, 'Item name must be at least 3 characters!')

        if len(request.POST['description']) < 3:
            messages.error(
                request, 'Description must be at least 3 characters!')

        error_messages = messages.get_messages(request)
        # don't clear messages due to them being accessed
        error_messages.used = False
        return len(error_messages) == 0


class Wish(models.Model):
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    is_granted = models.BooleanField(default=False)
    wished_by = models.ForeignKey(
        'User', related_name="wishes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="wishes_liked")
    objects = WishManager()
