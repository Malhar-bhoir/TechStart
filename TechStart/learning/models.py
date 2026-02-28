from django.db import models
from django.contrib.auth.models import User
# --- Add these imports at the top ---
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class LearningPath(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True) # 'computer' or 'programming'
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
# --- Level 2: The Specific Course (e.g. "Computer Basics", "Excel") ---
class Module(models.Model):
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    # UI: Icon for the card
    icon_svg = models.TextField(blank=True, help_text="SVG string for the module card")
    color_class = models.CharField(max_length=50, default="bg-blue-100 text-blue-600")

    def __str__(self):
        return self.name

class Topic(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    
    # UI Design elements from your views
    svg_path = models.TextField(help_text="Paste SVG path D attribute here")
    color_class = models.CharField(max_length=50, default="bg-blue-500", help_text="Tailwind bg color")
    
    # Content for the SLM to use
    content_summary = models.TextField(help_text="A brief summary of the topic for the SLM context")
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.name} - {self.name}"
class ChatMessage(models.Model):
    SENDER_CHOICES = [('user', 'User'), ('ai', 'AI')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    message = models.TextField()
    is_quiz = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    quiz_score = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'topic')



# --- Add this model at the bottom of the file ---

class UserProfile(models.Model):
    LANGUAGE_CHOICES = [
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Marathi', 'Marathi'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_language = models.CharField(
        max_length=20, 
        choices=LANGUAGE_CHOICES, 
        default='English'
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

# Signals to automatically create a profile when a User is created (via Google or Admin)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



