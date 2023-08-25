from rest_framework.generics import ListCreateAPIView, ListAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BannerSerializer, PostSerializer,PostCommentsSerializer,PostLikeSerializer, PollPostSerializer,PollPostRespondSerializer
from .models import Banner, Post, ImagePost, VideoPost, PollPost, PostComment, PostLike, PollPostRespond, ArticlePost
from accounts.models.models import User
from accounts.models.models2 import Follow
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

"""
BannerView
GetAllPost
PostImage
PostVideo
"""
class DefaultPagination(PageNumberPagination):
    page_size = 3

class BannerView(ListCreateAPIView):
    serializer_class = BannerSerializer
    queryset         = Banner.objects.all().order_by('id')
    pagination_class = DefaultPagination

@api_view(['GET'])
def get_active_banner(request):
    active = Banner.objects.filter(status=True).last()
    if active:
        return Response(data=BannerSerializer(active).data)
    else:
        return Response(status=404)

class BannerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BannerSerializer
    queryset         = Banner.objects.all()
    lookup_field     = 'id'
    pagination_class = DefaultPagination

class GetAllPost(APIView):
    serializer_class = PostSerializer
    pagination_class = DefaultPagination
    def get(self, request, user_id, format=None):
        try:
            user = User.objects.get(id=user_id)
            followings = Follow.objects.filter(following_user=user)
            
            queryset = Post.objects.none()
            for instance in followings:
                queryset |= Post.objects.filter(user=instance.followed_user)
            
            queryset = queryset.order_by('-id')
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            print('Query Set ::>> ',queryset)
            print('Paginated Query Set ::>> ',paginated_queryset)
            serializer = self.serializer_class(paginated_queryset, many=True, context={'user_id': user_id})

            response_data = {
                'count': queryset.count(),
                'results': serializer.data,
            }
            
            return Response(response_data, status=200)
        
        except User.DoesNotExist:
            return Response(status=404)
        except Exception as e:
            return Response(str(e), status=500)


class PostImage(APIView):
    def post(self, request):
        user_id = request.data.get("user")
        description = request.data.get("description")
        try:
            user_instance = User.objects.get(id=user_id)
            post_instance = Post.objects.create(
                user=user_instance, type="image", description=description
            )
        except:
            return Response(status=400, data={"message": "failed"})

        try:
            for i in range(len(request.FILES)):
                ImagePost.objects.create(
                    post=post_instance, image=request.FILES.get(f"image[{str(i)}]")
                )
        except:
            return Response(status=400, data={"message": "something went wrong"})

        return Response(status=200, data={"message": "sucess"})


class PostVideo(APIView):
    def post(self, request):
        user_id = request.data.get("user")
        description = request.data.get("description")
        try:
            user_instance = User.objects.get(id=user_id)
            post_instance = Post.objects.create(
                user=user_instance, type="video", description=description
            )
        except Exception as e :
            print('This is the Excetion ::>> ',e)
            return Response(status=400, data={"message": "failed"})
        try:
            VideoPost.objects.create(post=post_instance, video=request.FILES.get('video'))
        except Exception as e :
            return Response(status=400, data={"message": f" {e}"})
        return Response(status=200, data={"message": "success"})


class PostPoll(APIView):
    def post(self, request):
        user_id = request.data.get("user")
        optioncount = request.data.get("optionscount")
        subject = request.data.get("subject")
        options = []
        if "" in [user_id,optioncount,subject] and None in [user_id,optioncount,subject]:
            return Response(status=400, data={"message": "Bad request with some empty data field"})

        for count in range(1,int(optioncount)+1):
            if not request.data.get(f'option{count}') == '': 
                options.append(request.data.get(f'option{count}'))
            else:
                return Response(status=400, data={"message": f"Null option found ({count})"})

        try:
            user_instance = User.objects.get(id=user_id)
            post_instance = Post.objects.create(
                user=user_instance, 
                type="poll",
                poll_subject=subject,
            )
        except Exception as e :
            return Response(status=400, data={"message": f"{e}"})
        try:
            for option in options:
                PollPost.objects.create(post=post_instance,option=option)
        except Exception as e :
            return Response(status=400, data={"message": f" {e}"})
        return Response(status=200, data={"message": "success"})

class PostArticle(APIView):
    def post(self, request):
        user_id = request.data.get("user")
        body = request.data.get("body")
        try:
            user_instance = User.objects.get(id=user_id)
            post_instance = Post.objects.create(
                user=user_instance, type="article"
            )
        except:
            return Response(status=400, data={"message": "failed"})

        try:
            ArticlePost.objects.create(post=post_instance,body=body)
        except:
            return Response(status=400, data={"message": "something went wrong"})

        return Response(status=201, data={"message": "sucess"})


class PostCommentsView(ListCreateAPIView):
    serializer_class = PostCommentsSerializer
    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return PostComment.objects.filter(post__id=post_id)


class PostLikeView(ListCreateAPIView):
    serializer_class = PostLikeSerializer
    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return PostLike.objects.filter(post__id=post_id)

class PollPostRespondView(ListCreateAPIView):
    serializer_class = PollPostRespondSerializer
    queryset = PollPostRespond.objects.all()

    def create(self, request, *args, **kwargs):
        user_id = request.data.get('user')
        option_id = request.data.get('post_poll')
        selected_option = PollPost.objects.get(id=option_id)
        is_exist = PollPostRespond.objects.filter(post_poll__post__id=selected_option.post.id, user_id=user_id).exists()
        if is_exist:
           try:
                PollPostRespond.objects.get(post_poll__post__id=selected_option.post.id, user_id=user_id).delete()
                post_poll_instance = PollPost.objects.get(id=option_id)
                PollPostRespond.objects.create(post_poll=post_poll_instance,user=User.objects.get(id=user_id))
                instances = PollPost.objects.filter(post__id=post_poll_instance.post.id).order_by('id')
                options = []
                for instance in instances:
                    options.append(PollPostSerializer(instance).data)
                return Response(status=200,data=options)
           except Exception as e:
               print("Got an Exception -->>  ",e) 
               return Response(status=400,data={'message':'Something went wrong'})
        else:
            user = User.objects.get(id=user_id)
            post_poll = PollPost.objects.get(id=option_id)
            PollPostRespond.objects.create(user=user,post_poll=post_poll)
            instances = PollPost.objects.filter(post__id=post_poll.post.id).order_by('id')
            options = []
            for instance in instances:
                options.append(PollPostSerializer(instance).data)
            return Response(status=200,data=options)

 
@api_view(['POST'])
def un_like_post(request):
    user_id = request.data.get('user')
    post_id = request.data.get('post')
    is_post_exist = PostLike.objects.filter(post__id=post_id,user__id=user_id).exists()
    if is_post_exist:
        post_like_instance = PostLike.objects.get(post__id=post_id,user__id=user_id)
        post_like_instance.delete()
        return Response(status=204)
    else:
        return Response(status=404, data={"message": "given post not found"})
    

@api_view(["PUT", "PATCH"])
def like_post(request, id):
    is_post_exist = Post.objects.filter(id=id)
    if is_post_exist:
        post_instance = Post.objects.get(id=id)
        post_instance.like_count += 1
        post_instance.save()
        return Response(status=200)
    else:
        return Response(status=404, data={"message": "given post not found"})
