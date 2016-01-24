
from django.contrib import admin
from models import Unit, Test, SendingPrice, Range, TestGroup
from models import OtherLabs
from forms import AddTestForm

class TestInline(admin.StackedInline):
    model = Test
    extra = 0
class TestGroupAdmin(admin.ModelAdmin):
    inlines = [TestInline,]

class TestAdmin(admin.ModelAdmin):
    form = AddTestForm
    model = Test

admin.site.register(Unit)
admin.site.register(Test, TestAdmin)
admin.site.register(SendingPrice)
admin.site.register(Range)
admin.site.register(OtherLabs)
admin.site.register(TestGroup, TestGroupAdmin)

