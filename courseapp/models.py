from django.db import models


class Instructor(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Learner(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Course(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField()
	instructors = models.ManyToManyField(Instructor, blank=True)
	learners = models.ManyToManyField(Learner, blank=True)
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
	def is_get_score(self, selected_choice_ids):
		correct_choices = set(self.choice_set.filter(is_correct=True).values_list('id', flat=True))
		return set(selected_choice_ids) == correct_choices

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
