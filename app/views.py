from django.shortcuts import render
from app.models import Post, Comments
from app.forms import CommentForm, SubscribeForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    # Variables
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_modified')[0:3]
    subscribe_form = SubscribeForm()
    subscribe_success = None

    # Methods
    if request.method == 'POST':
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_success = 'Subscribed Successfully!'
            context = {
                'posts': posts,
                'top_posts': top_posts,
                'recent_posts': recent_posts,
                'subscribe_form': subscribe_form,
                'subscribe_success': subscribe_success
            }
    return render(request, 'app/index.html', context)

# Per individual Post page
def post_page(request, slug):
    # Variables
    post = Post.objects.get(slug=slug)
    form = CommentForm()
    comments = Comments.objects.filter(post=post, parent=None)

    #Methods
    # If a user makes a comment to a post
    if request.POST:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid:
            # Init object for now
            parent_object = None
            if request.POST.get('parent'):
                # save reply
                parent = request.POST.get('parent')
                # Get the parent obj(id) from the db and compare to the curr parent 
                parent_object = Comments.objects.get(id=parent)
                if parent_object: # If valid parent:
                    comment_reply = comment_form.save(commit=False)
                    comment_reply.parent = parent_object
                    comment_reply.post = post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))
            else:
                comment = comment_form.save(commit=False) # Dont save right away in db
                postid = request.POST.get('post_id')
                post = Post.objects.get(id = postid)
                comment.post = post # Logic to connect the comment to the post
                comment.save() # Now save to the db
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
