from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


# for this class we are extending the generic views and the generic view we
# are extending is the get method (list) and post method (create)
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

# we’ll have to make sure  comments are associated with a user upon creation.
# We do this with generics by  defining the perform_create method,
# which takes in self and serializer as arguments.  Inside, we pass in the
# user making the request as
# owner into the serializer’s save method, just  like we did in the regular
# class based views.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    filter_backends = [
        DjangoFilterBackend,
    ]

    filterset_fields = [
        # returns all comments associated with a post
        'post'
    ]

# Now, the CommentDetail view.  As we’d like to retrieve,
# update and delete a comment, I’ll extend  the RetrieveUpdateDestroyAPI
# generic view.
# We want only the comment owner to be able to edit  or delete it, so I’ll set
# the permission_classes
# to IsOwnerOrReadOnly. In order not to have to send  the post id every time
# I want to edit a comment,
# I’ll set serializer_class  to CommentDetailSerializer.
# Queryset will remain the same.
# Our serializer still needs to access the request,  but as mentioned
# before, we don’t really need to
# do anything, as the request is passed in  as part of the
# context object by default.


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
