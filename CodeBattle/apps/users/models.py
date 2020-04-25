from django.contrib.auth.models import AbstractBaseUser,    BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

  def _create_user(self, username,  email, password, is_staff, is_superuser, **extra_fields):
    if not email and not is_superuser:
        raise ValueError('Users must have an email address')
    if not username:
        raise ValueError('Users must have an username')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        username=username,
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        **extra_fields
    )
    
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self,username, email, password, **extra_fields):
    return self._create_user(email, password, False, False, **extra_fields)

  def create_superuser(self,username, password, **extra_fields):
    user=self._create_user(username,"", password, True, True, **extra_fields)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254, null=False, blank=True, default="Empty")
    sirname = models.CharField(max_length=254,null=False, blank=True,default="Empty")
    phone = models.CharField(max_length=15,null=False, blank=True,default="Empty")
    event_list = models.TextField(verbose_name="Список ID битв", null=True, unique=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name','sirname','phone']

    objects = UserManager()

    def getAcceptedEvents(self):
      return str(self.event_list).split(",")

    def removeEvent(self,id):
      if self.is_accepted_event(id):
        # lst = self.serializable_value(self.event_list).split(",")
        lst = str(self.event_list).split(",")
        lst.remove(str(id))
        self.event_list = ",".join(lst)
        self.save()
        return True
      return False    
      

    def addEvent(self,id):
      if not self.is_accepted_event(id):
        # lst = self.serializable_value(self.event_list).split(",")
        lst = str(self.event_list).split(",")
        lst.append(str(id))
        self.event_list = ",".join(lst)
        self.save()
        return True
      return False

    def is_accepted_event(self,id):
      # lst = self.serializable_value(self.event_list).split(",")
      
      lst = str(self.event_list).split(",")
      for elem in lst:
        if str(id) == elem:
          return True
      return False


    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)