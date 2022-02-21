
# 모델을 변경한 후에는 반드시 makemigrations와 migrate를 통해 데이터베이스를 변경해 주어야 한다.

from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200) # 제목은 최대 200자까지
    content = models.TextField()
    create_date = models.DateTimeField()
    # 제목처럼 글자수의 길이가 제한된 텍스트는 CharField를 사용해야 한다.
    # 내용(content)처럼 글자수를 제한할 수 없는 텍스트는 위처럼 TextField를 사용해야 한다.
    # 작성일시처럼 날짜와 시간에 관계된 속성은 DateTimeField를 사용해야 한다.
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question') # 추천인 추가

    def __str__(self):
        return self.subject


class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Question 모델을 속성으로, 기존 모델을 속성으로 연결하려면 ForeignKey를 사용
    # on_delete=models.CASCADE: 연결된 질문(Question)이 삭제될 경우 답변(Answer)도 함께 삭제된다
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
