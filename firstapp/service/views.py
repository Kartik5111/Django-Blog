from django.shortcuts import render,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import post
from django.contrib.auth.models import User

def home(request):

  context = {
        'posts': post.objects.all()
    }
  return render(request,"home.html",context)

class PostListView(ListView):
    model = post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by=5


class UserPostListView(ListView):
    model = post
    template_name = 'userpost.html' 
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = post
    template_name ='postdetail.html'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = post
    template_name ='postform.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = post
    template_name ='postform.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    template_name = 'postdelete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
def about(request):
    return render(request, 'about.html')

# Create your views here