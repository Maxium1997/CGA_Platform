from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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

    def get_object(self, queryset=None):
        topic = get_object_or_404(Topic, pk=self.kwargs.get('pk'))
        return topic


@method_decorator(login_required, name='dispatch')
class TopicWriteView(CreateView):
    model = Topic
    fields = ['title', 'content']
    template_name = 'cgaforum/topic_write.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicWriteView, self).get_context_data(object_list=None, **kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        criteria = Q(f=category) & Q(slug=self.kwargs.get('subcategory_slug'))
        subcategory = get_object_or_404(SubCategory, criteria)
        context['category'] = category
        context['subcategory'] = subcategory
        return context

    def get_initial(self):
        initial = super(TopicWriteView, self).get_initial()
        initial['subcategory'] = get_object_or_404(SubCategory, slug=self.kwargs.get('subcategory_slug'))
        return initial

    def form_valid(self, form):
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        criteria = Q(f=category) & Q(slug=self.kwargs.get('subcategory_slug'))
        subcategory = get_object_or_404(SubCategory, criteria)
        topic = form.instance
        topic.f = subcategory
        topic.created_by = self.request.user
        topic.save()
        return super(TopicWriteView, self).form_valid(form)
