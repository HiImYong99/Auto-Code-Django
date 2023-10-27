from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .forms import PostForm, CommentForm, TagForm
from django.core.exceptions import PermissionDenied
# Create your views here.


class PostListView(ListView):
    model = Post
    ordering = '-id'

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        if q:
            qs = qs.filter(title__icontains=q)
        return qs


postlist = PostListView.as_view()


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        '''
        여기서 원하는 쿼리셋이나 object를 추가한 후 템플릿으로 전달할 수 있습니다.
        '''
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
        video = form.save(commit=False)  # commit=False는 DB에 저장하지 않고 객체만 반환
        video.writer = self.request.user
        return super().form_valid(form)  # 이렇게 호출했을 때 저장합니다.

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('accounts:login'))


postcreate = PostCreateView.as_view()


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'file', 'category', 'tags']
    success_url = reverse_lazy('board:postlist')

    def test_func(self):
        return self.get_object().writer == self.request.user


postupdate = PostUpdateView.as_view()


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('board:postlsit')

    def test_func(self):
        return self.get_object().writer == self.request.user


postdelete = PostDeleteView.as_view()


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
