from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import *
from .filters import *
from .models import *


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = '-dateCreation'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all()
        return context

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})


class ComentList(ListView):
    model = Coment
    template_name = 'coment.html'
    context_object_name = 'coment'
    ordering = '-dateCreation'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        coments = Coment.objects.filter(post__author=self.request.user)
        self.filterset = ComentFilter(self.request.GET, queryset=coments)
        return self.filterset.qs

    def post(self, request, *args, **kwargs):
        coment_id = request.POST['coment']
        coment = Coment.objects.get(id=coment_id)
        if coment.accepted:
            coment.accepted = False
        else:
            coment.accepted = True
        coment.save()
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('/mycoments')


class ComentCreate(CreateView):
    model = Coment
    template_name = 'post.html'
    form_class = ComentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('coment_sent_for_approval')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = Post.objects.get(id=self.kwargs.get('pk'))
        self.object.accepted = False
        return super().form_valid(form)


class ComentForApproval(LoginRequiredMixin, ListView):
    model = Coment
    context_object_name = 'coments'
    template_name = 'comentsentforapproval.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetail(DetailView, ComentCreate):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'createpost.html'
    context_object_name = 'post_create'
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        self.object.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    raise_exception = True
    template_name = 'updatepost.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.get_full_path().split("/")[2])
        post.title = request.POST['title']
        post.text = request.POST['text']
        post.category = request.POST['category']
        post.save()
        return HttpResponseRedirect(f"../{post.id}")


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'deletepost.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_success_url(self):
        return reverse('posts')
