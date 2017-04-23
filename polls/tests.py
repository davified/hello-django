import datetime
from django.utils import timezone
from django.test import TestCase
from unittest import skip


from polls.models import Question

# imports for testing views
from django.test import Client

# Create your tests here.

class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(days=0.5)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view_returns_200_status_code(self):
        response = self.client.get('/polls/')
        self.assertEqual(response.status_code, 200)

    @skip("temporarily skipping test")
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed .
        """
        response = self.client.get('/polls/')
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


