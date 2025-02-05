from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)


# View for About Page
class AboutView(TemplateView):
    template_name = 'about.html'


# View for Post List Page (Updated)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # Specify template for the view
    context_object_name = 'posts'  # Define context variable
    
    def get_queryset(self):
        # Retrieve posts that are published (i.e., published_date is not null)
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


# View for Post Detail Page
class PostDetailView(DetailView):
    model = Post


# View for Creating a Post
class CreatePostView(LoginRequiredMixin, CreateView):
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


# View for Updating a Post
class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


# View for Deleting a Post
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


# View for Draft Posts
class DraftListView(ListView):
    model = Post
    template_name = 'blog/draft_list.html'

    def get_queryset(self):
        # Only retrieve posts that have not been published yet
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')


# View to Publish Post
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)  # Get the post by pk
    post.publish()  # This will set the published_date to the current time
    return redirect('post_detail', pk=post.pk)  # Redirect to the post detail page


# View for Adding a Comment to a Post
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # Link the comment to the post
            comment.save()
            return redirect('post_detail', pk=post.pk)  # Redirect back to the post detail page
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


# View to Approve a Comment
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()  # Approve the comment
    return redirect('post_detail', pk=comment.post.pk)  # Redirect to the post detail page


# View to Remove a Comment
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk  # Get the post's pk
    comment.delete()  # Delete the comment
    return redirect('post_detail', pk=post_pk)  # Redirect to the post detail page


# View to Create a New Post
@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save yet
            post.author = request.user  # Set the current user as the author
            post.save()  # Now save the post to the database
            return redirect('post_list')  # Redirect to the post list view or homepage
    else:
        form = PostForm()

    return render(request, 'blog/new_post.html', {'form': form})
