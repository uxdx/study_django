from django.contrib import admin
from .models import Choice, Question

class ChoiceInline(admin.TabularInline): 
    # admin.StackedInline 를 상속하면 좀 더 큼
    # admin.TabularInline 를 상속하면 좀 컴팩트함
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}), # fieldset 의 제목 지정(Date information)
    ]
    inlines = [ChoiceInline]
    """위 소소는 Django에게 《Choice 객체는 Question 관리자 페이지에서 편집된다. 
    기본으로 3가지 선택 항목을 제공함.》 이라고 알려줍니다.
    모양을 보려면 《Add question》 페이지를 로드하십시오.
    """

    list_display = ('question_text', 'pub_date', 'was_published_recently') # 열제목 표시
    list_filter = ['pub_date'] # 사이드바 필터를 사용할 수 있게
    search_fields = ['question_text'] # 검색바 추가

admin.site.register(Question, QuestionAdmin)