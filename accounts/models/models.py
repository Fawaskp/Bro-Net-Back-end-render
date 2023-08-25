from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta, date
from django.core.exceptions import ValidationError

"""
User
Badges
Hub
Batch
Stack
UserProfile
LogginWtithEmailData
"""


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise TypeError("Email Field Must Be Required")

        email = self.normalize_email(email)
        email = email.lower()
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("role", "super_user")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser field is_superuser must be True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    STUDENT = "student"
    COUNSELOR = "academic_counselor"
    COORDINATOR = "review_coordinator"
    ADMIN = "brototype_admin"
    SUPERUSER = "super_user"

    ROLE_CHOICES = (
        (STUDENT, "Student"),
        (COUNSELOR, "Academic Counselor"),
        (COORDINATOR, "Review Coordinator"),
        (ADMIN, "Brototype Admin"),
        (SUPERUSER, "Super User"),
    )

    fullname = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True, blank=True)
    email = models.EmailField(
        max_length=200, unique=True, db_index=True, null=False, blank=True
    )
    role = models.CharField(
        default="student", max_length=200, choices=ROLE_CHOICES, blank=True
    )
    is_verified = models.BooleanField(default=False, blank=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_staff = models.BooleanField(default=False, blank=True)
    is_superuser = models.BooleanField(default=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    is_profile_completed = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        # if self.dob and self.dob > date.today() - timedelta(days=6205):
        #      raise ValidationError('You should be at least 17 years old to register.')
        # print('Self.Dob  = ',self.dob)
        # print('Date today : ',date.today())
        # print('Deff : ', date.today() - timedelta(days=6205))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Badges(models.Model):
    name = models.CharField(max_length=50)
    icon = models.ImageField(upload_to="badge-icons", null=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Badges"

    def __str__(self):
        return self.name


class Hub(models.Model):
    location = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self) -> str:
        return f"{self.location} ({self.code})"


class Batch(models.Model):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(unique=True)
    batch_name = models.CharField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.batch_name:
            batch_number = self.number
            if self.number < 10:
                batch_number = "0" + str(self.number)
            self.batch_name = f"{self.hub.code}{batch_number}".upper()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "batches"

    def __str__(self) -> str:
        return self.batch_name


class Stack(models.Model):
    name = models.CharField(max_length=20, unique=True)
    icon = models.ImageField(upload_to="stack-icons", null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    profile_image = models.ImageField(upload_to="profiles", null=True)
    stack = models.ForeignKey(Stack, on_delete=models.CASCADE, null=True)
    about = models.TextField(null=True)
    personal_website = models.CharField(max_length=200, null=True)
    communication_cord = models.BooleanField(default=False)
    tech_cord = models.BooleanField(default=False)
    following_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    badges = models.ManyToManyField(Badges, blank=True)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, null=True, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    skills = models.ManyToManyField('accounts.Skill', blank=True)

    def __str__(self) -> str:
        return self.user.fullname


class LoginWithEmailData(models.Model):
    email = models.CharField(max_length=50, default="not given")
    time = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=50)

    def __str__(self):
        return f"LoginWithEmailData {self.pk}"

    def get_time_elapsed(self):
        now = timezone.now()
        elapsed_time = now - self.time
        elapsed_minutes = elapsed_time.total_seconds() // 60
        return elapsed_minutes

    def __str__(self):
        return f"LoginWithEmailData {self.pk}"


class EmailChangeOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    new_email = models.CharField(max_length=50,null=True)
    otp = models.CharField(max_length=4)
    time = models.TimeField(auto_now_add=True)



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
