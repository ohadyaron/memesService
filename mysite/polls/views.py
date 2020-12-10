import mimetypes
import os

from django.conf import settings
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Mem, Image


def load_images():
    for file in os.listdir(settings.STATICFILES_DIRS[0] + settings.IMAGES_DIR):
        print("inserted " + file)
        try:
            Image.objects.get_or_create(path=settings.IMAGES_DIR + file)
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


class ImageView(generic.DetailView):
    model = Image
    template_name = 'polls/image.html'


class MemView(generic.DetailView):
    model = Mem
    template_name = 'polls/mem.html'


def set_text(request, image_id):
    selected_image = get_object_or_404(Image, pk=image_id)
    try:
        print("new mem " + selected_image.path)
        upper_text = request.POST.get('utext')
        lower_text = request.POST.get('ltext')
        mem = Mem.objects.get_or_create(image=selected_image,
                                        upper_text=upper_text,
                                        lower_text=lower_text)[0]
        mem.path = settings.MEMES_DIR + str(mem.id) + '.jpg'
        mem.save()
        Mem.generate_meme(image_path=settings.STATICFILES_DIRS[0] + selected_image.path,
                          font_path=settings.STATICFILES_DIRS[0] + '/fonts/impact/impact.ttf',
                          dst_path=settings.STATICFILES_DIRS[0] + mem.path,
                          top_text=upper_text,
                          bottom_text=lower_text)
        return HttpResponseRedirect(reverse('polls:meme', args=(mem.id,)))
    except (KeyError, Mem.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/image.html', {
            'mem': image_id,
            'error_message': "You didn't select a text.",
        })


def download(request, mem_id):
    file_path = settings.STATICFILES_DIRS[0] + settings.MEMES_DIR + str(mem_id) + '.jpg'
    print('download ' + file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            mime_type, _ = mimetypes.guess_type(file_path)
            response = HttpResponse(fh.read(), content_type=mime_type)
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            return response
    raise Http404


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
