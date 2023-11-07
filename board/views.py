from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.db.models import Q
from datetime import date
from django.db.models import Count

# Create your views here.


class PostListView(ListView):
    model = Post
    ordering = '-id'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_posts'] = Post.objects.annotate(
            like_count=Count('like_user')).filter(like_count__gte=0).order_by('-created_at')[:5]
        context['today'] = date.today()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '')
        c = self.request.GET.get('c', '')
        s = self.request.GET.get('s', '')
        if q or c:
            qs = qs.filter(Q(title__icontains=q) & Q(category__icontains=c))
        if s:
            if s == 'desc':
                return Post.objects.all().order_by('-id')
            elif s == 'asc':
                return Post.objects.all().order_by('id')
            elif s == 'like':
                return Post.objects.annotate(like_count=Count('like_user')).order_by('-like_count')
            elif s == 'view':
                return Post.objects.all().order_by('-view_count')
            else:
                return Post.objects.all().order_by('-id')

        return qs


postlist = PostListView.as_view()


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def get_object(self, queryset=None):
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
        post = form.save(commit=False)
        post.writer = self.request.user
        return super().form_valid(form)

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


class PostCommentView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CommentForm

    def form_valid(self, form):
        commentForm = form.save(commit=False)
        commentForm.post = self.get_object()
        commentForm.writer = self.request.user
        commentForm.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('board:postdetail', args=[self.get_object().pk])

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse_lazy('accounts:login'))


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_id = comment.post.id
    comment.delete()
    return redirect('board:postdetail', post_id)


def likes(request, pk):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=pk)
        if post.like_user.filter(pk=request.user.pk).exists():
            post.like_user.remove(request.user)
        else:
            post.like_user.add(request.user)
        return redirect('board:postdetail', pk=pk)
    return redirect('accounts:login')
