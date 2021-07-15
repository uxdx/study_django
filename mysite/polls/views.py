from django.shortcuts import render

# Create your views here.
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, loader

from .models import Choice, Question
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

# ! 비효율 적인 방식
# def index(request):
#     # latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     # template = loader.get_template('polls/index.html')
#     # context = {'latest_question_list': latest_question_list,}
#     # return HttpResponse(template.render(context, request))
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

# ! 더 효율적인 방식
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self): # 오버라이드
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question # Question 모델은 context로 따로 지정해주디않아도 자동으로 제공됨
    template_name = 'polls/detail.html'
    """
    기본적으로 DetailView 제너릭 뷰는 <app name>/<model name>_detail.html 템플릿을 사용합니다.
    우리의 경우에는 "polls/question_detail.html"템플릿을 사용할 것입니다. 
    template_name 속성은 Django에게 자동 생성 된 기본 템플릿 이름 대신에 특정 템플릿 이름을 사용하도록 알려주기 위해 사용됩니다. 
    results리스트 뷰에 대해서 template_name을 지정합니다 - 결과 뷰와 상세 뷰가 렌더링 될 때 서로 다른 모습을 갖도록합니다. 
    이들이 둘다 동일한 DetailView를 사용하고 있더라도 말이지요.

    """
    def get_queryset(self): # 오버라이드
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        # POST자료에서 choice를 가져옴
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') + 1
        # F 함수는 경쟁상태(Avoid Race Condition)를 피하기 위해 사용
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # 사용자가 url로 리다이랙트 됨
        # POST 데이터를 성공적으로 다룬 후에는 반드시 HttpResponseRedirect를 해야함.
