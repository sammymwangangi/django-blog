from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.dates import WeekArchiveView
from .models import Post

def index(request):
	context = {
		'posts': Post.objects.all()
	}
	return render(request, 'djapp/index.html', context)

class PostListView(ListView):
	model = Post
	template_name = 'djapp/index.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post
	template_name = 'djapp/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 3

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
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
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostWeekArchiveView(WeekArchiveView):
	queryset = Post.objects.all()
	date_field = "date_posted"
	week_format = "%W"
	allow_future = True

def about(request):
	return render(request, 'djapp/about.html', {'title': 'About'})

def contact(request):
	return render(request, 'djapp/contact.html')
