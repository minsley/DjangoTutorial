from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from polls.models import Poll

# # Create your views here.
# def index(request):
# 	latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
# 	## Can make this shorter by using the django 'render' shortcut instead 
# 	## of an HttpResponse
# 	# template = loader.get_template('polls/index.html')
# 	# context = RequestContext(request, {
# 	# 	'latest_poll_list': latest_poll_list
# 	# })
# 	# return HttpResponse(template.render(context))
# 	context = {'latest_poll_list': latest_poll_list}
# 	return  render(request, 'polls/index.html', context)

# def detail(request, poll_id):
# 	## Can make this shorter also by using a 404 shortcut
# 	# try:
# 	# 	poll = Poll.objects.get(pk=poll_id)
# 	# except Poll.DoesNotExist:
# 	# 	raise Http404
# 	poll = get_object_or_404(Poll, pk=poll_id)
# 	return render(request, 'polls/details.html', {'poll': poll})

# def results(request, poll_id):
# 	# return HttpResponse("You're looking at the results of poll %s" % poll_id)
# 	poll = get_object_or_404(Poll, pk=poll_id)
# 	return render(request, 'polls/results.html', {'poll':poll})

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_poll_list'

	def get_queryset(self):
		# """Return the last five published polls."""
		# return Poll.objects.order_by('-pub_date')[:5]
		"""
		Return the last five published polls (not including those set to be published in the future).
		"""
		return Poll.objects.filter(
			pub_date__lte=timezone.now()
			).order_by('-pub_date')[:5]
		
class DetailView(generic.DetailView):
	model = Poll
	template_name = 'polls/details.html'

	def get_queryset(self):
		"""
		Excludes any polls that aren't published yet.
		"""
		return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Poll
	template_name = 'polls/results.html'

def vote(request, poll_id):
	p = get_object_or_404(Poll, pk=poll_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the poll voting form.
		return render(request, 'polls/detail.html', {
			'poll': p,
			'error_message': "You didn't select a choice.",
			})
	else: 
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpsResponseRedirect after successfully dealing 
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))