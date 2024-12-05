from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Topic, Category, SubCategory, Post, Comment, Profile
from django.db.models import Count
from django.core.paginator import Paginator
from .forms import CreateTopicForm, CreatePostForm, CreateCommentForm, ProfileForm
from .mixins import ProfileAndLoginRequired, AuthorOrSuperuserPermissionMixin
# Create your views here.


class HomepageView(ListView):
    model = Category
    template_name = 'forum/homepage.html'
    context_object_name = 'categories'

    @method_decorator(cache_page(60*30))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Category.objects.prefetch_related('subcategory').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Головна сторінка'
        return context


class CategoryTopicsView(ListView):
    model = Topic
    template_name = 'forum/category-topics.html'
    context_object_name = 'topics'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return Topic.objects.filter(subcategory__category=self.category).annotate(count_posts=Count('posts'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Список обговорень {self.category.name}'
        context['category_title'] = self.category.name
        return context


class SubcategoryTopicsView(ListView):
    model = Topic
    template_name = 'forum/category-topics.html'
    context_object_name = 'topics'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        self.subcategory = get_object_or_404(SubCategory, slug=self.kwargs['subcategory_slug'], category=self.category)
        return Topic.objects.filter(subcategory=self.subcategory).annotate(count_posts=Count('posts'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Список обговорень {self.subcategory.name}'
        context['category_title'] = self.subcategory.name
        context['category_slug'] = self.category.slug
        context['subcategory_slug'] = self.subcategory.slug
        return context


class TopicView(DetailView):
    model = Topic
    template_name = 'forum/topicview.html'
    context_object_name = 'topic'

    def get_object(self):
        category_slug = self.kwargs['category_slug']
        subcategory_slug = self.kwargs['subcategory_slug']
        return get_object_or_404(Topic, id=self.kwargs['topic_id'],
                                 subcategory__slug=subcategory_slug,
                                 subcategory__category__slug=category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        topic = context['topic']

        posts = Post.objects.filter(topic=topic).order_by('-created_at') \
            .select_related('author__profile') \
            .prefetch_related('comments__author__profile')

        context['posts'] = posts

        paginator = Paginator(posts, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj.object_list

        return context


class ProfileView(ProfileAndLoginRequired, DetailView):
    model = Profile
    template_name = 'forum/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        profile_id = self.kwargs.get('profile_id')
        if profile_id:
            obj = get_object_or_404(Profile, id=profile_id)
            return obj
        else:
            return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['profile'].user
        context['title'] = 'Профіль користувача'
        context['user_topics'] = Topic.objects.filter(author=user)
        return context


class CreateProfileView(ProfileAndLoginRequired, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'forum/createprofile.html'

    def form_valid(self, form):
        profile = form.save(commit=False)
        profile.user = self.request.user
        profile.filled = True
        profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('my-profile')


class CreateTopicView(ProfileAndLoginRequired, CreateView):
    model = Topic
    form_class = CreateTopicForm
    template_name = 'forum/createtopic.html'

    def dispatch(self, request, *args, **kwargs):
        self.subcategory = get_object_or_404(SubCategory, slug=kwargs['subcategory_slug'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.subcategory = self.subcategory
        topic.author = self.request.user
        topic.save()
        return super().form_valid(form)


class CreatePostView(ProfileAndLoginRequired, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'forum/createpost.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.topic = get_object_or_404(Topic, id=self.kwargs['topic_id'])
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('topic', kwargs={'category_slug': self.kwargs['category_slug'],
                                        'subcategory_slug': self.kwargs['subcategory_slug'],
                                        'topic_id': self.kwargs['topic_id']})


class CreateCommentView(ProfileAndLoginRequired, CreateView):
    model = Comment
    form_class = CreateCommentForm
    template_name = 'forum/createcomment.html'

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.author = self.request.user
        comment.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('topic', kwargs={'category_slug': self.kwargs['category_slug'],
                                        'subcategory_slug': self.kwargs['subcategory_slug'],
                                        'topic_id': self.kwargs['topic_id']})


class DeletePostView(ProfileAndLoginRequired, AuthorOrSuperuserPermissionMixin, DeleteView):
    model = Post
    template_name = 'forum/deleteform.html'
    id_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse('topic', kwargs={'category_slug': self.kwargs['category_slug'],
                                        'subcategory_slug': self.kwargs['subcategory_slug'],
                                        'topic_id': self.kwargs['topic_id']})


class DeleteCommentView(ProfileAndLoginRequired, AuthorOrSuperuserPermissionMixin, DeleteView):
    model = Comment
    template_name = 'forum/deleteform.html'
    id_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('topic', kwargs={'category_slug': self.kwargs['category_slug'],
                                        'subcategory_slug': self.kwargs['subcategory_slug'],
                                        'topic_id': self.kwargs['topic_id']})


class DeleteTopicView(ProfileAndLoginRequired, AuthorOrSuperuserPermissionMixin, DeleteView):
    model = Topic
    template_name = 'forum/deleteform.html'
    id_url_kwarg = 'topic_id'

    def get_success_url(self):
        return reverse('subcategory-topics', kwargs={'category_slug': self.kwargs['category_slug'],
                                                     'subcategory_slug': self.kwargs['subcategory_slug']})


class UpdateProfileView(ProfileAndLoginRequired, UpdateView):
    model = Profile
    template_name = 'forum/update-profile.html'
    form_class = ProfileForm

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        return reverse('my-profile')
