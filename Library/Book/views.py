from .models import Book,User
from .serializers import BookSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import CustomPagination


class RegisterView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status': 403,'errors': serializer.errors,'message':'Invalid username or password'})
        serializer.save()

        user=User.objects.get(username=serializer.data['username'])
        token_obj, _ = Token.objects.get_or_create(user=user)
        return Response({'status': 200, 'payload': serializer.data, 'token':str(token_obj)})


class BookCreateList(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=Book.objects.all()
    serializer_class = BookSerializer
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def post(self, request, *args, **kwargs):
        response=super().post(request,*args, **kwargs)
        return Response({"message":"created new book","status":200})

class BookList(generics.ListAPIView):
    queryset=Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = CustomPagination

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            if instance.author != request.user:
                raise Exception("User is not the author of this Book")
            return super().patch(request,*args,**kwargs)
        except Exception as e:
            return Response({'error':str(e)})

    def put(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            if instance.author != request.user:
                raise Exception("User is not the author of this Book")
            return super().put(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)})

    def delete(self,request,*args,**kwargs):
        try:
            instance = self.get_object()
            if instance.author != request.user:
                raise Exception("User is not the author of this Book")
            response=super().delete(request, *args, **kwargs)
            return Response({'message':'Book Deleted'})
        except Exception as e:
            return Response({'error': str(e)})


# Create your views here.
