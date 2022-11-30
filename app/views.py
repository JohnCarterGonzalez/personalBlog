from django.shortcuts import render
from app.models import Post
from app.forms import CommentForm

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'app/index.html', context)

# Per individual Post page
def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    form = CommentForm()
    # Check the view_count for the post, if there isnt any views, add 1
    # If there is more than one view, increment by one, save to db
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()
    context = {'post': post, 'form': form}
    return render(request, 'app/post.html', context)
