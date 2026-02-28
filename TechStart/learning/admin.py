from django.contrib import admin
from .models import LearningPath, Module, Topic, UserProgress

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'slug')
    list_filter = ('path',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    # Changed 'path' to 'module' to match the new model structure
    list_display = ('name', 'module', 'order') 
    list_filter = ('module',)
    ordering = ('module', 'order')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'completed', 'quiz_score')