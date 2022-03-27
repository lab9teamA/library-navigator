from django.shortcuts import render

def page_not_found_view(request, exception):
    print("In page not found")
    return render(request, '404.html', status=404)