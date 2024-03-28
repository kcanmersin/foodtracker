from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .models import UserAccount
from .serializers import UserAccountSerializer
from rest_framework import generics
#permission import
from rest_framework import permissions

#permission classes is open for all user

class UserListView(generics.ListAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [permissions.AllowAny]

    #permission_classes = [permissions.IsAuthenticated]  # Sadece doğrulanmış kullanıcıların erişimine izin ver

class UserDetailView(generics.RetrieveAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [permissions.AllowAny]
    
    #permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'  # Kullanıcıyı belirli bir alanla arayın, örneğin 'username' ya da 'email' de olabilir

#list all users
class UserProfileView(generics.RetrieveAPIView):
        queryset = UserAccount.objects.all()
        serializer_class = UserAccountSerializer
        permission_classes = [permissions.AllowAny]
            
        #permission_classes = [permissions.IsAuthenticated]
        lookup_field = 'username'  # Kullanıcıyı belirli bir alanla arayın, örneğin 'username' ya da 'email' de olabilir
        def get_object(self):
            queryset = self.get_queryset()
            obj = get_object_or_404(queryset, username=self.kwargs['username'])
            return obj