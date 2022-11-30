from django.shortcuts import render
from app.models import Post, Comments
from app.forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'app/index.html', context)

# Per individual Post page
def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    form = CommentForm()
    comments = Comments.objects.filter(post=post)

    # If a user makes a comment to a post
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            comment = comment_form.save(commit=False) # Dont save right away in db
            postid = request.POST.get('post_id')
            post = Post.objects.get(id = postid)
            comment.post = post # Logic to connect the comment to the post
            comment.save() # Now save to the sb
            # Keep the comments from submitting with page refresh
            return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

    # Check the view_count for the post, if there isnt any views, add 1
    # If there is more than one view, increment by one, save to db
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()
    context = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'app/post.html', context)
