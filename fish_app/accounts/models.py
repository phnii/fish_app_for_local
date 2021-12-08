from django.contrib.auth.models import AbstractUser, BaseUserManager  
from django.db import models  

class CustomUserManager(BaseUserManager): 
    use_in_migrations = True 
   
    def _create_user(self, email, password, **extra_fields):
       if not email:
          raise ValueError('The given email must be set')
       email = self.normalize_email(email)
       user = self.model(email=email, **extra_fields)
       user.set_password(password)
       user.save(using=self._db)
       return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
        
    def create_superuser(self, email, password, **extra_fields):
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_superuser', True)
      if extra_fields.get('is_staff') is not True:
          raise ValueError('Superuser must have is_staff=True.')
      if extra_fields.get('is_superuser') is not True:
          raise ValueError('Superuser must have is_superuser=True.')
      return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'
    email = models.EmailField('メールアドレス', unique=True)
    introduce = models.TextField('自己紹介',max_length=300, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

class Connection(models.Model):
    follower = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followed', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} : {}'.format(self.follower.username, self.followed.username)

class Room(models.Model):
    users = models.ManyToManyField(CustomUser)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser, related_name='sender', on_delete=models.CASCADE)
    content = models.TextField(max_length=600)
    room = models.ForeignKey(Room, related_name='room', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
