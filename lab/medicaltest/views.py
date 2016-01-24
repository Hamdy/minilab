from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from models import Test
from models import TestGroup
from medicaltest.forms import AddTestForm
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse

@user_passes_test(lambda u: u.is_superuser)
def tests(request, param=''):
    if request.method == "POST":
        param = request.POST.get("param")
    if param:
        tests = Test.objects.filter(name__contains=param)
        groups = TestGroup.objects.filter(name__contains=param)
        tests_in_groups = Test.objects.filter(group__in=groups)
        from itertools import chain
        tests = sorted(list(chain(tests, tests_in_groups)))
    else:
        tests = Test.objects.all()
    
    return render(request, 'tests.html', {'tests':tests})

@user_passes_test(lambda u: u.is_superuser)
def edit(request, id=''):
    return HttpResponseRedirect('/admin/medicaltest/test/' + str(id))

@user_passes_test(lambda u: u.is_superuser)
def add(request):
    return HttpResponseRedirect('/admin/medicaltest/test/add')

@user_passes_test(lambda u: u.is_superuser)
def confirm_delete(request, id=0):
    test = get_object_or_404(Test, pk=id)
    test.delete()
    return HttpResponseRedirect(reverse('list_tests'))

@user_passes_test(lambda u: u.is_superuser)
def delete(request, id=0):
    test = get_object_or_404(Test, pk=id)
    return render(request, 'delete_test.html', {'test':test})

