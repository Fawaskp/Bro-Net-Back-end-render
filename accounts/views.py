from rest_framework.generics import ListAPIView,ListCreateAPIView,CreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models.models import User,UserProfile,Hub,Batch,Stack
from .models.models2 import Dos,Donts,Message
from .serializers.serializers import UserSearchSerializer, UserDetailSerializer,UserProfileSerializer,\
HubSerializer,BatchSerializer, StackSerializer,DosSerializer,DontsSerializer,MessageSerializer,ChatListSerializer
from .permission import IsAuthenticatedWithToken
from rest_framework import filters
from django.db.models import Q,F

'''
ViewUsers
UserDetail
ViewUserProfile
UserProfileDetail

GetStackList
GetHubList
GetBatchList

Dos and Don'ts
'''

class SearchUser(ListAPIView):
    serializer_class = UserSearchSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['fullname', 'username', 'email']

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id is not None:
            queryset = User.objects.exclude(id=user_id)
        return queryset

class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'id'

class ViewUserProfile(CreateAPIView):
    queryset = UserProfile.objects.all()

class UserProfileDetail(APIView):
    permission_classes = [IsAuthenticatedWithToken]
    def put(self, request ,id):
        try:
            user_profile = UserProfile.objects.get(user_id=id)
        except:
            return Response({'Message' : 'Data Not Found',"status":status.HTTP_404_NOT_FOUND})
        
        serializer = UserProfileSerializer(user_profile, data=request.data)
        # print('Request Data : ',request.data)
        if serializer.is_valid():
            serializer.save()
            user_profile.is_profile_completed = True
            user_profile.save()
            user = User.objects.get(id=id)
            user.is_profile_completed = True
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'Message' : serializer.errors,"status":status.HTTP_400_BAD_REQUEST})
        
    def get(self, request, id):
        try:
            user_profile = UserProfile.objects.get(user_id=id)
        except:
            return Response({'Message': 'Data Not Found',"status":status.HTTP_404_NOT_FOUND})
        else:
            serializer = UserProfileSerializer(user_profile)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

class GetStackList(ListAPIView):
    queryset = Stack.objects.all()
    serializer_class = StackSerializer

class GetHubList(ListAPIView):
    queryset = Hub.objects.all()
    serializer_class = HubSerializer

class GetBatchList(ListAPIView):
    serializer_class = BatchSerializer
    def get_queryset(self):
        hub_id = self.request.query_params.get('hub_id', '')
        if hub_id and Hub.objects.filter(id=hub_id).exists() :
            hub_instance = Hub.objects.get(id=hub_id)
            return Batch.objects.filter(hub=hub_instance)
        return {}

class DosView(ListCreateAPIView):
    serializer_class = DosSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id and Dos.objects.filter(user_id=user_id).exists() :
            return Dos.objects.filter(user_id = user_id)
        return []

class DontsView(ListCreateAPIView):
    serializer_class = DontsSerializer
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id and Donts.objects.filter(user_id=user_id).exists() :
            return Donts.objects.filter(user_id = user_id)
        return []
    
class DosDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Dos.objects.all()
    serializer_class = DosSerializer
    lookup_field = 'id'

class DontsDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Donts.objects.all()
    serializer_class = DontsSerializer
    lookup_field = 'id'

class PreviousMessagesView(ListAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        thread_suffix = f"{user1}_{user2}" if user1 > user2 else f"{user2}_{user1}"
        thread_name = 'chat_'+thread_suffix
        queryset = Message.objects.filter(
            thread_name=thread_name
        )
        return queryset

class ChatListView(ListAPIView):
    serializer_class = ChatListSerializer

    def get_queryset(self):
        user_id = int(self.kwargs['user_id'])
        distinct_senders = Message.objects.filter(receiver__id=user_id).values('sender__username').distinct()
        distinct_receivers = Message.objects.filter(sender__id=user_id).values('receiver__username').distinct()

        distinct_usernames = set()
        for entry in distinct_senders:
            distinct_usernames.add(entry['sender__username'])

        for entry in distinct_receivers:
            distinct_usernames.add(entry['receiver__username'])
        return distinct_usernames