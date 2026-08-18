from django.http import HttpResponse
import time 


class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("Request Path:", request.path)

        if request.path == "/blocked/":
            return HttpResponse("Access Denied")
         
        response = self.get_response(request)
 
        print(response)
        return response


def request_logging_middleware(get_response):

    def middleware(request):

        print("Method:", request.method)
        print("Path:", request.path)
        print("User: ",request.user)
        print("GET : ",request.GET)
        response = get_response(request)

        return response

    return middleware

def timing_middleware(get_response):

    def middleware(request):

        start_time = time.time()

        response = get_response(request)

        end_time = time.time()

        execution_time = end_time - start_time

        print("Execution Time:", execution_time)

        return response

    return middleware


def custom_header_middleware(get_response):

    def middleware(request):

        response = get_response(request)

        response["X-App"] = "1.0"
        print("responseeee")
        print(response)
        return response

    return middleware


BLOCKED_IPS = {
    "192.168.2.168",
    
}


def ip_filter_middleware(get_response):

    def middleware(request):

        ip = request.META.get("REMOTE_ADDR")
      

        if ip in BLOCKED_IPS:
            return HttpResponse(
                "Access Denied",
                status=403
            )

        return get_response(request)

    return middleware