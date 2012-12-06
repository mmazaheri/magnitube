from django.shortcuts import render
from django.http import HttpResponseRedirect

from formats import FORMATS

import urlparse
import subprocess as sub
import re

def index(request):
	return render(request, "downloader/index.html", {})
	
def process_download_request(request):
	if request.method == 'POST' and 'url' in request.POST:
		url = request.POST['url']
		url_data = urlparse.urlparse(url)
		url_qs = urlparse.parse_qs(url_data.query)
		
		if 'v' in url_qs and re.match('^[-\w]+$', url_qs['v'][0]):
			video_id = url_qs['v'][0]
			return HttpResponseRedirect('/%s/' % video_id)
		
	return render(request, "downloader/index.html", {})	

def show_list(request, video_id):
	p = sub.Popen(["youtube-dl", "--all-formats", "-g", "--get-format", "--get-filename",
		"http://www.youtube.com/watch?v=%s" % video_id],
		stdout=sub.PIPE,
		stderr=sub.PIPE)
	
	output, errors = p.communicate()
	output = output.split('\n')
	
	print output
	
	links = []
	
	for i in range(len(output) / 3):
		links.append([output[3*i], output[3*i + 1], output[3*i + 2]])
	
	try:
		del request.session['links']
	except:
		pass
		
	request.session['links'] = links
	
	return render(request, "downloader/download_links.html", {'links': links, 'video_id': video_id})	
	

def download(request, video_id, id):
	pass
	