from django.contrib import admin
from DomainIdeas.models import Word, DomainName

# Register your models here.

class DomainNameInLine(admin.TabularInline):
	model = DomainName
	extra = 3

class WordAdmin(admin.ModelAdmin):
	list_display = ('spelling', 'definition')
	list_filter = ['spelling']
	search_fields = ['spelling', 'definition']
	inlines = [DomainNameInLine]

admin.site.register(Word, WordAdmin)