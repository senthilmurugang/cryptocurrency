from django.http import HttpResponse
def home(request):
    return HttpResponse("<h3>Your app is working</h3>")
def test(request):
    return HttpResponse("<h3>This is a test page<h3>")
def static_content(request):
    return HttpResponse("<p>This is a static content</p>")
def json_response(request):
    return HttpResponse("{'url':'"+str(request.path_info)+"','isSucess':'true'}")