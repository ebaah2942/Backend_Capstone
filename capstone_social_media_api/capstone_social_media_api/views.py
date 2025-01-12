from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        "Message": "Welcome to  Capstone Social Media API"
    })
