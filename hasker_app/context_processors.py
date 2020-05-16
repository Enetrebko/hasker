from . import models


def trending_questions(request):
    return {'trending_questions': models.Question.objects.order_by('-votes', '-created_date')}