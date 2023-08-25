from django.db import models
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import UserProfile

'''
Social-Media
Uesr-Social-Media
Skill
Project
Education-Category
User-Education
WorkExperience
Follow
Dos
Donts
'''

class SocialMedia(models.Model):
    icon = models.ImageField(upload_to='social-media-icons',blank=True)
    name = models.CharField(max_length=20,unique=True,blank=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = ("Socila Media")

    def __str__(self) -> str:
        return self.name

class UserSocialMediaAccounts(models.Model):
    social_media = models.ForeignKey(SocialMedia,on_delete=models.CASCADE,blank=True)
    user         = models.ForeignKey("accounts.User",on_delete=models.CASCADE,blank=True)
    url          = models.CharField(max_length=80,blank=True)

    class Meta:
        unique_together = ('social_media', 'user')

    def __str__(self) -> str:
        return f"{self.user.username} ({self.social_media.name})"

class Skill(models.Model):
    name  = models.CharField(max_length=30,blank=True)
    icon  = models.ImageField('skill-icons',blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['id']

class Project(models.Model):
    user            = models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    name            = models.CharField(max_length=50,unique=True)
    description     = models.TextField()
    logo            = models.ImageField('project-logo',null=True)
    repository_link = models.CharField(max_length=80)
    live_link       = models.CharField(max_length=50)
    skills_used     = models.ManyToManyField(Skill)

    class Meta:
        ordering = ['id']
        verbose_name_plural = ("Projects")

    def __str__(self):
        return f"{self.name} by {self.user.fullname}"


class ProjectAdditionalSkills(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=50)


class EducationCategory(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name
    

class UserEducation(models.Model):
    category    = models.ForeignKey(EducationCategory,on_delete=models.SET_NULL,null=True,blank=True)
    user        = models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    course      = models.CharField(max_length=100,null=True)
    location    = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.category.name +' of ' + self.user.username
    
    class Meta:
        ordering = ['id']

class WorkExperience(models.Model):
    user     = models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    company  = models.CharField(max_length=100)
    position = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.user.username + self.position + ' at ' + self.company 


class Follow(models.Model):
    following_user = models.ForeignKey("accounts.User",on_delete=models.CASCADE,related_name='following_user_set')
    followed_user  = models.ForeignKey("accounts.User",on_delete=models.CASCADE,related_name='followed_user_set')

    class Meta:
        unique_together = ['following_user', 'followed_user']

    def __str__(self) -> str:
        return f"{self.following_user} followed {self.followed_user}"


class Dos(models.Model):
    user  = models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    title = models.CharField(max_length=50,null=True)
    do    = models.TextField()

    def __str__(self) -> str:
        return f"Do of {self.user}" 


class Donts(models.Model):
    user  = models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    title = models.CharField(max_length=50,null=True)
    dont  = models.TextField()

    def __str__(self) -> str:
        return f"Dont's of {self.user}" 
    

class Message(models.Model):
    sender = models.ForeignKey("accounts.User", on_delete=models.CASCADE, null=True, blank=True,related_name="sender_message_set")
    receiver = models.ForeignKey("accounts.User", on_delete=models.CASCADE, null=True, blank=True,related_name="reciever_message_set")
    message = models.TextField(null=True, blank=True)
    thread_name = models.CharField(null=True, blank=True, max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.sender.username}-{self.thread_name}' if self.sender else f'{self.message}-{self.thread_name}'



@receiver(post_save, sender=Follow)
def update_follow_counts(sender, instance, created, **kwargs):
    if created:

        followed_user = instance.followed_user
        following_user = instance.following_user

        followed_user_profile = UserProfile.objects.get(user=followed_user)
        followed_user_profile.followers_count += 1 
        followed_user_profile.save()

        following_user_profile = UserProfile.objects.get(user=following_user)
        following_user_profile.following_count += 1
        following_user_profile.save()

        
@receiver(post_delete, sender=Follow)
def update_follow_counts_on_delete(sender, instance, **kwargs):
    followed_user = instance.followed_user
    following_user = instance.following_user

    followed_user_profile = UserProfile.objects.get(user=followed_user)
    followed_user_profile.followers_count -= 1
    followed_user_profile.save()

    following_user_profile = UserProfile.objects.get(user=following_user)
    following_user_profile.following_count -= 1
    following_user_profile.save()