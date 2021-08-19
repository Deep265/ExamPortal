from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.urls import reverse_lazy
# Http imports
from  django.http import HttpResponseRedirect
# Models and forms import
from .models import Post,Comments
# Views import
from django.views.generic import TemplateView,ListView,DeleteView,UpdateView,DetailView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Random imports
from django.utils import timezone
# Create your views here.
class About(TemplateView):
    template_name = 'blog_site/about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now())

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/authorize/login/'
    model = Post
    template_name = 'blog_site/draft_list.html'
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-created_date')

class PostDetailView(DetailView):
    model = Post

@login_required
def PostCreateView(request):
    if request.method == "POST":
        title = request.POST.get('title')
        text = request.POST.get('text')
        p = Post(user=request.user,title=title,text=text)
        p.save()
        return HttpResponseRedirect(reverse('blog:post_list'))
    return render(request,'blog_site/post_create.html')
@login_required
def publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog:post_list')

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/authorize/login/'
    model = Post
    fields = ('title','text')

class PostDeleteView(DeleteView,LoginRequiredMixin):
    login_url = 'authorize/login/'
    success_url = reverse_lazy('blog:post_list')
    model = Post
# Comments Views

def add_comments(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":

        author = request.POST.get('author')
        text = request.POST.get('text')

        c = Comments(post=post,author=author,text=text)
        c.save()
        return redirect('blog:post_detail',pk=post.pk)
    return render(request,'blog_site/comments.html')
@login_required
def DeleteComment(request,pk):
    comment = get_object_or_404(Comments,pk=pk)
    post_key = comment.post.pk
    comment.delete()                    # post_key saves the commet pk
    return redirect('blog:post_detail',pk=post_key)
@login_required
def approve_comment(request,pk):
    comment = get_object_or_404(Comments,pk)
    comment.approve_comments()
    return redirect('blog:post_detail',pk=comment.post.pk)











