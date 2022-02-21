from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count

from ..models import Question


def index(request):
    3 / 0  # 강제로 오류발생
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    # GET 방식으로 호출된 URL에서 page값을 가져올 때 사용
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.objects.order_by('-create_date')

    # 검색
    # 질문 목록 데이터 얻기. order_by('-create_date')는 작성일시 역순으로 정렬하라는 의미
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)
    # paginator를 이용하여 요청된 페이지(page)에 해당되는 페이징 객체(page_obj)를 생성
    # 장고 내부적으로는 데이터 전체를 조회하지 않고 해당 페이지의 데이터만 조회하도록 쿼리가 변경된다.
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    # render 함수는 파이썬 데이터를 템플릿에 적용하여 HTML로 반환하는 함수.
    # 사용한 render 함수는 question_list 데이터를 pybo/question_list.html 파일에 적용하여 HTML을 리턴
    # pybo/question_list.html과 같은 파일을 템플릿(Template)이라고 부른다. 장고에서 사용하는 태그를 사용할수 있는 HTML 파일
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    """
    pybo 내용 출력
    """
    # Question.objects.get(id=question_id)를 get_object_or_404(Question, pk=question_id)로 바꾸어 주었다.
    # 여기서 사용한 pk는 Question 모델의 기본키(Primary Key)인 id를 의미
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)