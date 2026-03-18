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
	selected_choice_ids = list(selected_choices.values_list('id', flat=True))
	total = questions.count()
	score = 0
	for question in questions:
		user_selected = [cid for cid in selected_choice_ids if Choice.objects.get(id=cid).question_id == question.id]
		if question.is_get_score(user_selected):
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
