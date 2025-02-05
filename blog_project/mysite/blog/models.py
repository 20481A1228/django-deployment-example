from django.db import models
from django.utils import timezone
from django.urls import reverse

# Post Model
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    def approved_comment_count(self):
        """Return the number of approved comments for the post."""
        return self.comments.filter(approved_comment=True).count()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

# Comment Model
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)  # ForeignKey to Post model
    author = models.CharField(max_length=200)  # The author of the comment
    text = models.TextField()  # The content of the comment
    create_date = models.DateTimeField(default=timezone.now)  # The time when the comment was created
    approved_comment = models.BooleanField(default=False)  # Whether the comment has been approved

    def approve(self):
        """Approve the comment, marking it as approved."""
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        """Return the URL to access the post detail page after the comment is created."""
        return reverse('post_detail', kwargs={'pk': self.post.pk})

    def __str__(self):
        """Return the text of the comment as its string representation."""
        return self.text
