from rest_framework.decorators import api_view
from rest_framework.response import Response


# the message can say anything you need it to
@api_view()
def root_route(request):
    return Response({
        'message': "Welcome to my drf API!!"
    })
