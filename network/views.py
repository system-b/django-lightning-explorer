from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from network.models import *
from backend.lib.utils import *

def index(request, query=False):
	page = int(request.GET.get('page', 1)) 
	page_count, total_count = 0, 0
	
	node_count = Node.objects.all().count()
	channel_count = Channel.objects.all().count()
	
	if query:
		try:
			node = Node.objects.get(Q(nodeid=query) | Q(alias=query))
			
			return redirect(node.get_url())
		except Exception as e:
			node_query = Node.objects.filter(Q(nodeid__icontains=query) | Q(alias__icontains=query))
			
			total_count = node_query.count()
			node_list = node_query.order_by('-last_timestamp')[(page-1)*settings.PER_PAGE:page*(settings.PER_PAGE)]
	else:
		total_count = Node.objects.all().count()
		
		node_list = Node.objects.filter().order_by('-last_timestamp')[page*settings.PER_PAGE:(page+1)*(settings.PER_PAGE)]
	
	pagination = Pagination(page, settings.PER_PAGE, total_count)
	page_count = total_count/page
	
	return render(request, 'index.jinja', {
		'node_count': node_count,	
		'channel_count': channel_count,	
		
		'query': query,	
		'node_list': node_list,	
		
		'page_count': page_count,	
		'pagination': pagination,	
	})

def node_view(request, nodeid):
	node_count = Node.objects.all().count()
	channel_count = Channel.objects.all().count()
	
	node = get_object_or_404(Node, nodeid=nodeid)
	
	return render(request, 'node_view.jinja', {
		'node_count': node_count,	
		'channel_count': channel_count,	
		
		'query': nodeid,	
		'node': node
	})
	
def sitemap(request):
	location_list = [
		'https://'+settings.ALLOWED_HOSTS[0],
	]

	node_list = Node.objects.all()

	for _ in node_list:
		location_list.append('https://'+settings.ALLOWED_HOSTS[0]+_.get_url())

	return render(request, 'sitemap.xml', dict(
		location_list=location_list,
	), content_type="application/xhtml+xml")
