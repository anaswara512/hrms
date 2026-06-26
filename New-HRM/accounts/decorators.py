from django.http import HttpResponse

def hr_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return HttpResponse("Please login first")

        if request.user.role != 'HR':
            return HttpResponse("Access Denied. HR Only")

        return view_func(request, *args, **kwargs)

    return wrapper