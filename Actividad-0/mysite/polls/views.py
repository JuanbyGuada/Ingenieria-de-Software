from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Choice, Question

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context={"latest_question_list":latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question":question})


def results(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question":question})

def vote(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        # Muestra el formulario de votacion de nuevo
        return render(request, "polls/detail.html", {
            "question":question,
            "error_message":"No seleccionaste una opcion.",
        })
    else:
        selected_choice.votes=F("votes")+1
        selected_choice.save()
        # Siempre retornar un HttpResponseRedirect despues de tratar con exito
        # los datos de un formulario POST. Esto previene que los datos sean
        # posteados dos veces si un usuario presiona el boton de regreso.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))