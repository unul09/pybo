from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request):
    """
    pybo 질문등록
    """
    # 질문 등록 화면에서 subject, content 항목에 값을 기입하고 "저장하기" 버튼을 클릭하면
    # 동일한 /pybo/question/create/ 페이지가 POST방식으로 요청된다.
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # 대신 form.save()를 수행하면 Question 모델의 create_date에 값이 없다는 오류가 발생
            # subject, content 속성만 정의되어 있고 create_date 속성은 없기 때문
            # 이러한 이유로 임시 저장을 한 후
            # question 객체를 리턴받아 create_date에 값을 설정한 후 question.save()로 실제 저장하는 것이다.
            question = form.save(commit=False)
            question.author = request.user
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')

    # 질문 목록 화면에서 "질문 등록하기" 버튼을 클릭한 경우에는
    # /pybo/question/create/ 페이지가 GET 방식으로 요청되어 question_create 함수가 실행된다.
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')



