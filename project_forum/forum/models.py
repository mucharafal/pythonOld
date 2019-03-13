from django.db import models
from django.contrib.auth.models import User, Group


# Create your models here.

class Forum(models.Model):
    title = models.CharField(max_length=50, verbose_name="Tytuł")
    slug = models.SlugField('Odnośnik', unique=False, max_length=100)
    forum = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "Forum"
        verbose_name_plural = "Fora"
        unique_together = ('slug', 'forum')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Thread(models.Model):
    title = models.CharField(max_length=50, verbose_name="Tytuł")
    slug = models.SlugField('Odnośnik', unique=False, max_length=100)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Wątek"
        verbose_name_plural = "Wątki"
        unique_together = ('slug', 'forum')

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField("Data dodania")
    text = models.TextField("Treść")
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posty"

    def __unicode__(self):
        return self.thread + "-" + self.author + "-" + self.date





