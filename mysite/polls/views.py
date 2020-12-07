from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Mem, Image


def load_images():
    print("XXXX")
    from django.contrib.staticfiles.utils import get_files
    from django.contrib.staticfiles.storage import StaticFilesStorage

    s = StaticFilesStorage()
    for file in list(get_files(s, location='mysite')):
        try:
            Image.objects.get_or_create(path=file)
            print("inserted " + file)
        except (KeyError, Image.DoesNotExist):
            print("already exists " + file)


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_images_list'

    load_images()

    def get_queryset(self):
        """Return 20 static images."""
        return Image.objects.all()


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


class MemView(generic.DetailView):
    model = Mem
    template_name = 'polls/image.html'


def set_text(request, image_id):
    image = get_object_or_404(Mem, pk=image_id)
    try:
        image.upper_text(pk=request.POST['utext'])
        image.lower_text(pk=request.POST['ltext'])
    except (KeyError, Mem.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'image': image,
            'error_message': "You didn't select a text.",
        })
    else:
        image.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:memes', args=(image.id,)))


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
