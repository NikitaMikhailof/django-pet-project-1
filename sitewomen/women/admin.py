from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet, Q
from .models import Women, Category


admin.site.site_header = 'Панель администрирвоания'


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщины'
    parameter_name = 'status'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужеи')
        ]
    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'content', 'cat', 'husband', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    # filter_horizontal = ['tags']
    list_display = ('id', 'title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    list_editable = ('is_published', )
    ordering = ('-time_create', 'title')
    actions = ['set_published', 'set_draft']
    list_per_page = 5
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter, 'cat__name', 'is_published']

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info (self, women:Women):
        return f'Описание {len(women.content)} символов'
    
    @admin.action(description='Опубликовать')
    def set_published(self, request, queryset):
       count =  queryset.update(is_published=Women.Status.PUBLISHED)
       self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.action(description='Снять с публикации')
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} записи(ей) сняты с публикации!", messages.WARNING)


@admin.register(Category)
class WomenAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
   