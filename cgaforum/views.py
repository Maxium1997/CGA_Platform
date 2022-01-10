from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView


from cgaforum.models import Category, SubCategory
# Create your views here.


class CategoriesView(ListView):
    model = Category


class SubCategoriesView(ListView):
    model = SubCategory

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SubCategoriesView, self).get_context_data(object_list=None, **kwargs)
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        context['category'] = category
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return SubCategory.objects.filter(f=category)
