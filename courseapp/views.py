from django.shortcuts import render, get_object_or_404, redirect
from .models import Lesson, Question, Choice, Submission
from django.http import HttpResponse

def submit(request, lesson_id):
	lesson = get_object_or_404(Lesson, pk=lesson_id)
	if request.method == 'POST':
		selected_choices = request.POST.getlist('choices')
		submission = Submission.objects.create(user=request.user.username if request.user.is_authenticated else 'guest', lesson=lesson)
		for choice_id in selected_choices:
			submission.choices.add(choice_id)
		submission.save()
		return redirect('show_exam_result', submission_id=submission.id)
	questions = Question.objects.filter(lesson=lesson)
	return render(request, 'courseapp/exam_form.html', {'lesson': lesson, 'questions': questions})

def show_exam_result(request, submission_id):
	submission = get_object_or_404(Submission, pk=submission_id)
	lesson = submission.lesson
	questions = Question.objects.filter(lesson=lesson)
	selected_choices = submission.choices.all()
	total = questions.count()
	score = 0
	for question in questions:
		correct_choices = set(question.choice_set.filter(is_correct=True))
		user_choices = set(selected_choices.filter(question=question))
		if correct_choices == user_choices:
			score += 1
	percent = int((score / total) * 100) if total > 0 else 0
	passed = percent >= 70
	return render(request, 'courseapp/exam_result.html', {
		'submission': submission,
		'lesson': lesson,
		'score': score,
		'total': total,
		'percent': percent,
		'passed': passed,
		'questions': questions,
		'selected_choices': selected_choices,
	})
