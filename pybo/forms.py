from django import forms
from pybo.models import Question, Answer, Comment


# QuestionForm은 모델 폼(forms.ModelForm)을 상속
# 모델 폼(forms.ModelForm): 모델(Model)과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할수 있는 폼
class QuestionForm(forms.ModelForm):
    # Meta 클래스에는 사용할 모델과 모델의 속성을 적어야 한다.
    class Meta:
        model = Question
        fields = ['subject', 'content']

        labels = {
            'subject': '제목',
            'content': '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }