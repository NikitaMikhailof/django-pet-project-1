from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'


    title = models.CharField(max_length=255, verbose_name='название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='слаг')
    content = models.TextField(blank=True, verbose_name='описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='дата обновления')
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="статус")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='категория')
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name='теги')
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='wumen', verbose_name='муж')

    objects = models.Manager()
    published = PublishedManager()
    
    class Meta:
        verbose_name = 'Известные женщины мира'
        verbose_name_plural = 'Известные женщины мира'
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug}) 

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title, allow_unicode=True)
    #     super().save(*args, **kwargs)


    def __str__(self):
        return self.title


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag

class Husband(models.Model):
    name = models.CharField(max_length=100)    
    age = models.IntegerField(null=True)    
    m_count = models.IntegerField(blank=True, default=0)
    
    def __str__(self):
        return self.name