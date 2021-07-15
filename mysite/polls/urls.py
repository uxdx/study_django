from django.urls import path

from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # 제너릭 뷰를 사용했기때문에 URL의 인수를 pk로 가져옴
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    # 기본 뷰 방식이기때문에 question_id에 URL의 인수가 담겨옴
]