from django.db import models
from django.utils.text import slugify

# Create your models here.
class Tag(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	slug = models.SlugField(max_length=200, unique=True)

	"""
	Override the default slug save method, if the slug is not specified
	then create a slug using slugify. Save the new slug with return super()
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
