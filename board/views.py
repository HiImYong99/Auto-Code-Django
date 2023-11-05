from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.db.models import Q
from datetime import date
# Create your views here.


class PostListView(ListView):
    model = Post
    ordering = '-id'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        c = self.request.GET.get('c', '')
        if q or c:
            qs = qs.filter(Q(title__icontains=q) & Q(category__icontains=c))
        return qs


postlist = PostListView.as_view()


class PopularPostListView(ListView):
    model = Post
    ordering = '-id'
    paginate_by = 5
    template_name = 'board/popular_post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['today'] = date.today()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        c = self.request.GET.get('c', '')
        if q or c:
            qs = qs.filter(Q(title__icontains=q) & Q(category__icontains=c))
        return qs


popular_postlist = PopularPostListView.as_view()


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def get_object(self, queryset=None):
        '''
        말 그대로 PostDetailView.as_view()에서 사용할 object를 반환합니다.
        반환 하는데 object를 변경할 수 있는 함수입니다.
        여기서 원하는 쿼리셋이나 object를 추가한 후 템플릿으로 전달할 수 있습니다.
        '''
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        post.view_count += 1
        post.save()
        return super().get_object(queryset)


postdetail = PostDetailView.as_view()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('board:postlist')

    def form_valid(self, form):
        post = form.save(commit=False)  # commit=False는 DB에 저장하지 않고 객체만 반환
        post.writer = self.request.user
        return super().form_valid(form)  # 이렇게 호출했을 때 저장합니다.

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('accounts:login'))


postcreate = PostCreateView.as_view()


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'img', 'category']
    success_url = reverse_lazy('board:postlist')

    def test_func(self):
        return self.get_object().writer == self.request.user


postupdate = PostUpdateView.as_view()


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('board:postlist')

    def test_func(self):
        return self.get_object().writer == self.request.user

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.test_func():
            self.object.delete()
            return HttpResponseRedirect(self.get_success_url())


post_delete = PostDeleteView.as_view()


@login_required
def comment_new(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # commit=False는 DB에 저장하지 않고 객체만 반환
            comment = form.save(commit=False)
            comment.post = post
            comment.writer = request.user
            comment.save()
            return redirect('board:postdetail', pk)
    else:
        form = CommentForm()
    return render(request, 'board/post_form.html', {
        'form': form,
    })


def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_id = comment.post.id
    comment.delete()
    return redirect('board:postdetail', post_id)


@login_required
def likes(request, pk):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=pk)
        if post.like_user.filter(pk=request.user.pk).exists():
            post.like_user.remove(request.user)
        else:
            post.like_user.add(request.user)
        return redirect('board:postdetail', pk=pk)
    return redirect('accounts:login')
