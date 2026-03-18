from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission, Instructor, Learner

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 2

class QuestionInline(admin.TabularInline):
	model = Question
	extra = 1

class QuestionAdmin(admin.ModelAdmin):
	inlines = [ChoiceInline]
	list_display = ('text', 'lesson', 'grade')

class LessonAdmin(admin.ModelAdmin):
	inlines = [QuestionInline]
	list_display = ('title', 'course')

class LessonInline(admin.TabularInline):
	model = Lesson
	extra = 1

class CourseAdmin(admin.ModelAdmin):
	inlines = [LessonInline]
	list_display = ('name', 'description')

class SubmissionAdmin(admin.ModelAdmin):
	list_display = ('user', 'lesson', 'submitted_at')

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
