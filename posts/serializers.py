from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import Banner,Post,ImagePost,VideoPost,ArticlePost,PollPost,PostComment,PostLike,PollPostRespond
from accounts.serializers.serializers import UserViewSerializer, UserProfileSerializer
from accounts.models.models import UserProfile, User

class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class ImagePostSerializer(ModelSerializer):
    class Meta:
        model = ImagePost
        fields = ['post','image']

class VideoPostSerializer(ModelSerializer):
    class Meta:
        model = VideoPost
        fields = '__all__'

class ArticlePostSerializer(ModelSerializer):
    class Meta:
        model = ArticlePost
        fields = '__all__'

class PollPostSerializer(ModelSerializer):
    class Meta:
        model = PollPost
        fields = '__all__'

class PollPostRespondSerializer(ModelSerializer):
    class Meta:
        model = PollPostRespond
        fields = '__all__'

class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'

class PostCommentsSerializer(ModelSerializer):
    user_detail = SerializerMethodField()
    class Meta:
        model  = PostComment
        fields = '__all__' 
    
    def get_user_detail(self,obj):
        result = {}
        result.update(fullname=UserViewSerializer(obj.user).data.get('fullname'))
        result.update(username=UserViewSerializer(obj.user).data.get('username'))
        userprofile_instance = UserProfile.objects.get(user=obj.user)
        result.update(profile_image=UserProfileSerializer(userprofile_instance).data.get('profile_image'))
        return result

class PostSerializer(ModelSerializer):
    post = SerializerMethodField()
    user = SerializerMethodField()
    is_liked = SerializerMethodField()
    poll_selected_option = SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'
    
    def get_post(self,obj):
        if obj.type == 'image':
            post = []
            instances = ImagePost.objects.filter(post=obj)
            for instance in instances:
                post.append((ImagePostSerializer(instance).data.get('image')))
            return post
        elif obj.type == 'video':
            try:
                return [VideoPostSerializer(VideoPost.objects.get(post=obj)).data.get('video')]
            except:
                return []
        elif obj.type == 'poll':
            post = []
            instances = PollPost.objects.filter(post=obj).order_by('id')
            for instance in instances:
                post.append((PollPostSerializer(instance).data))
            return post
        elif obj.type == 'article':
            try:
                return [ArticlePostSerializer(ArticlePost.objects.get(post=obj)).data.get('body')]
            except:
                return []
            
    
    def get_user(self,obj):
        result = {}
        result.update(id=UserViewSerializer(obj.user).data.get('id'))
        result.update(fullname=UserViewSerializer(obj.user).data.get('fullname'))
        result.update(username=UserViewSerializer(obj.user).data.get('username'))
        userprofile_instance = UserProfile.objects.get(user=obj.user)
        result.update(profile_image=UserProfileSerializer(userprofile_instance).data.get('profile_image'))
        return result

    def get_is_liked(self,obj):
        user = User.objects.get(id=self.context.get('user_id'))    
        return PostLike.objects.filter(user=user,post=obj).exists()
    
    def get_poll_selected_option(self,obj):
        if obj.type == 'poll':
            user = User.objects.get(id=self.context.get('user_id'))   
            is_exist = PollPostRespond.objects.filter(user=user,post_poll__post__id=obj.id).exists()
            if is_exist:
                instance = PollPostRespond.objects.get(user=user,post_poll__post__id=obj.id)
                return PollPostRespondSerializer(instance).data.get('post_poll')
            return None
        else:
            return None
        
