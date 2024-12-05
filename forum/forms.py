from django.forms.models import ModelForm
from .models import Topic, Post, Comment, Profile


class CreateTopicForm(ModelForm):

    class Meta:
        model = Topic
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'title_input', 'placeholder': 'Введіть назву теми'})
        self.fields['content'].widget.attrs.update({'class': 'content_textarea', 
                                                    'placeholder': 'Введіть ваше запитання',
                                                    })
        self.fields['title'].label = 'Заголовок обговорення'
        self.fields['content'].label = 'Текст запитання'


class CreatePostForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ['content']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = 'Тест поста'
        self.fields['content'].widget.attrs.update({'class': 'content-textarea'})


class CreateCommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = 'Тест поста'
        self.fields['content'].widget.attrs.update({'class': 'content-textarea'})


class ProfileForm(ModelForm):

    class Meta:
        model = Profile

        fields = ['first_name', 'last_name', 'bio']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['first_name'].label = "Ім'я"
            self.fields['last_name'].label = "Прізвище"
            self.fields['bio'].label = 'Біографія'

