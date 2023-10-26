from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
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


postdetail = PostDetailView.as_view()


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'file', 'category', 'tags']
    success_url = reverse_lazy('postlist')


postcreate = PostCreateView.as_view()


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'file', 'category', 'tags']
    success_url = reverse_lazy('postlist')


postupdate = PostUpdateView.as_view()


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('postlsit')


postdelete = PostDeleteView.as_view()
