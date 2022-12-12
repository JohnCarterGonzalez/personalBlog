from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count

from app.forms import CommentForm, SubscribeForm
from app.models import *


# Create your views here.
def index(request):
    # Variables
    posts = Post.objects.all()
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_modified')[0:3]
    featured_posts = Post.objects.filter(is_featured=True)
    subscribe_form = SubscribeForm()
    subscribe_success = None
    website_info = None
    # Methods
    """
    For the user, if the request is POST and valid, then save the email to th e
    db and reset the form.
    """
    if request.POST:
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_success = 'Subscribed Successfully!'
            subscribe_form = SubscribeForm() # Reset the form if successful

    """
    If there are mutiple featured posts competing for the top spot then take
    first in the list. Essentially, featured_posts is not an object but a query
    set, thus the need to filter.
    """
    if featured_posts:
        featured_posts = featured_posts[0]

    """
    First check to see if the WebsiteMeta exists, we dont want a crash simply
    b/c of being absentminded. lets handle that here.
    """
    if WebsiteMeta.objects.exists():
        website_info = WebsiteMeta.objects.all()[0]

    context = {
                'posts': posts,
                'top_posts': top_posts,
                'recent_posts': recent_posts,
                'subscribe_form': subscribe_form,
                'subscribe_success': subscribe_success,
                'featured_posts': featured_posts,
                'website_info': website_info
            }
    return render(request, 'app/index.html', context)

# Per individual Post page
def post_page(request, slug):
    # Variables
    post = Post.objects.get(slug=slug)
    top_posts = Post.objects.all().order_by('-view_count')[0:3]
    recent_posts = Post.objects.all().order_by('-last_modified')[0:3]
    form = CommentForm()
    comments = Comments.objects.filter(post=post, parent=None)
    # tag = Tag.objects.get(slug=slug)
    # top_related_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2]

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
                comment.post = post  # Logic to connect the comment to the post
                comment.save()  # Now save to the db
                # Keep the comments from submitting with page refresh
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

    # Check the view_count for the post, if there isnt any views, add 1
    # If there is more than one view, increment by one, save to db
    if post.view_count is None:
        post.view_count = 1
    else:
        post.view_count = post.view_count + 1
    post.save()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
        'top_posts': top_posts,
        'recent_posts': recent_posts,
        #'tag': tag,
        #'top_related_posts': top_related_posts,
    }
    return render(request, 'app/post.html', context)

# Define the Tag Page
def tag_page(request, slug):
	# Objects
	tag = Tag.objects.get(slug=slug)
	tags = Tag.objects.all()

	# Filter the top_posts and the recent_posts for frontend view
	top_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:2]
	recent_posts = Post.objects.filter(tags__in=[tag.id]).order_by('-last_modified')[0:2]

	context = {
                'tag': tag,
			    'top_posts': top_posts,
			    'recent_posts': recent_posts,
			    'tags': tags}
	return render(request, 'app/tag.html', context)

# Define the Bio section for Authors page 
def author_page(request, slug):
    profile = Profile.objects.get(slug=slug)

    # Filter the top_posts and the recent_posts for frontend view
    top_posts = Post.objects.filter(author = profile.user).order_by('-view_count')[0:2]
    recent_posts = Post.objects.filter(author = profile.user).order_by('-last_modified')[0:2]
    # For the possibility of a side bar, not yet implemented.
    # top_authors = User.objects.annotate(number=Count('post')).order_by('number')

    context = {'profile': profile, 'top_posts': top_posts, 'recent_posts': recent_posts}
    return render(request, 'app/author.html', context)

def search_page(request):
    search_query = ''
    # If the request has the param q, if so then get th evalue of q
    # q is the text entered in the search box 
    if request.GET.get('q'):
        search_query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=search_query)
    print('Search: ', search_query)
    context = {
        'posts': posts,
        'search_query': search_query
    }
    return render(request, 'app/search.html', context)

def about_page(request):
    website_info = None

    """
    First check to see if the WebsiteMeta exists, we dont want a crash simply
    b/c of being absentminded. lets handle that here.
    """
    if WebsiteMeta.objects.exists():
        website_info = WebsiteMeta.objects.all()[0]

    context={
			'website_info': website_info
			}
    return render(request, 'app/about.html', context)
