from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


from cga_case.models import CaseCategory, CaseSection, Case
# Create your views here.


class CaseCategoriesView(ListView):
    model = CaseCategory


class CaseSectionsView(ListView):
    model = CaseSection

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CaseSectionsView, self).get_context_data(object_list=None, **kwargs)
        context['category'] = self.kwargs.get('category_name')
        return context

    def get_queryset(self):
        category = get_object_or_404(CaseCategory, name=self.kwargs.get('category_name'))
        return CaseSection.objects.filter(is_part_of=category)


class CaseDetailView(DetailView):
    model = Case

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CaseDetailView, self).get_context_data(object_list=None, **kwargs)
        case = get_object_or_404(Case, title=self.kwargs.get('case_title'))
        context['category'] = case.is_one_of.is_part_of
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Case, title=self.kwargs.get('case_title'))


@method_decorator(login_required, name='dispatch')
class CaseUpdateView(UpdateView):
    model = Case
    fields = ['handling_point', 'cautions', 'flow_chart']
    template_name = 'cga_case/case_update.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return super(CaseUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CaseUpdateView, self).get_context_data(object_list=None, **kwargs)
        case = get_object_or_404(Case, title=self.kwargs.get('case_title'))
        context['category'] = case.is_one_of.is_part_of
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Case, title=self.kwargs.get('case_title'))

    def get_success_url(self):
        case = self.get_object()
        return reverse_lazy('case_update', kwargs={'case_title': case.title})
