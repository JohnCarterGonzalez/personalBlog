from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Profile for Authors
class Profile(models.Model):
# users have one profle and a profile has one user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    slug = models.SlugField(max_length=200, unique=True)
    profile_bio = models.CharField(max_length=200)

    """
    Override the default slug save method, if the slug is not specified
    then create a slug using slugify. Save the new slug with return super().save()
    """
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)

# Return a string representation of the slug
    def __str__(self):
        return self.user.first_name

# Class Subscribe
class Subscribe(models.Model):
    email = models.EmailField(max_length=100)
    date = models.DateField(auto_now_add=True)

# Tag Model
class Tag(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	slug = models.SlugField(max_length=200, unique=True)

	"""
	Override the default slug save method, if the slug is not specified
	then create a slug using slugify. Save the new slug with return super().save()
	"""
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		return super(Tag, self).save(*args, **kwargs)

	# Return a string representation of the slug
	def __str__(self):
		return self.name

# Post Model
class Post(models.Model):
	title = models.CharField(max_length=200)
	content = models.TextField()
	last_modified = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(max_length=200, unique=True)
	image = models.ImageField(null=True, blank=True, upload_to="images/")
	tags = models.ManyToManyField(Tag, blank=True, related_name="post")
	view_count = models.IntegerField(null=True, blank=True)
	is_featured = models.BooleanField(default=False)
	author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

class Comments(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # Link to the reply to the post, related_name specifies the replies against the comments queries
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='replies')

class WebsiteMeta(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    about = models.TextField()
