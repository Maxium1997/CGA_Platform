from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q

from cgaforum.models import Category, SubCategory, Topic
from cgaforum.definitions import TopicStatus
# Create your views here.


class CategoriesView(ListView):
    model = Category


class SubCategoriesView(ListView):
    model = SubCategory

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SubCategoriesView, self).get_context_data(object_list=None, **kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        context['category'] = category
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        return SubCategory.objects.filter(f=category)


class TopicsView(ListView):
    model = Topic

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicsView, self).get_context_data(object_list=None, **kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        criteria = Q(f=category) & Q(slug=self.kwargs.get('subcategory_slug'))
        subcategory = get_object_or_404(SubCategory, criteria)
        context['category'] = category
        context['subcategory'] = subcategory
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        subcategory_criteria = Q(f=category) & Q(slug=self.kwargs.get('subcategory_slug'))
        subcategory = get_object_or_404(SubCategory, subcategory_criteria)
        topic_criteria = Q(f=subcategory) & (Q(status=TopicStatus.Published.value[0]) | Q(status=TopicStatus.Privacy.value[0]))
        return Topic.objects.filter(topic_criteria).order_by('-published_time')


class TopicView(DetailView):
    model = Topic

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicView, self).get_context_data(object_list=None, **kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        criteria = Q(f=category) & Q(slug=self.kwargs.get('subcategory_slug'))
        subcategory = get_object_or_404(SubCategory, criteria)
        context['category'] = category
        context['subcategory'] = subcategory
        return context
