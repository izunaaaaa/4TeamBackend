from rest_framework.serializers import ModelSerializer
from .models import Recomment
from users.serializers import TinyUserSerializer

class RecommentSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    
    class Meta:
        model = Recomment
        fields = (        
        "user",
                  "created_at",
        "description",
        "comment",)
