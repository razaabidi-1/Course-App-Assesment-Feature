from django.db import models

class Course(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	def __str__(self):
		return self.name

class Lesson(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	content = models.TextField()
	def __str__(self):
		return self.title

class Question(models.Model):
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
	text = models.CharField(max_length=500)
	grade = models.IntegerField(default=1)
	def __str__(self):
		return self.text

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	text = models.CharField(max_length=200)
	is_correct = models.BooleanField(default=False)
	def __str__(self):
		return self.text

class Submission(models.Model):
	# For simplicity, we use a CharField for user; in real apps, use ForeignKey to User
	user = models.CharField(max_length=100)
	lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
	choices = models.ManyToManyField(Choice)
	submitted_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"Submission by {self.user} for {self.lesson.title}"
