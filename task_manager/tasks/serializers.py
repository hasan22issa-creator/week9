from rest_framework import serializers
from .models import Task
 
 
# A serializer is the translator between Python objects and JSON.
# It works exactly like a ModelForm but for APIs instead of HTML forms.
# It converts:  Task object  →  JSON  (when sending data out)
# And:          JSON  →  Task object  (when receiving data in)
 
class TaskSerializer(serializers.ModelSerializer):
 
    # owner is read-only — we set it automatically, the user never sends it
    owner = serializers.StringRelatedField(read_only=True)
 
    # created_at is set automatically — user shouldn't be able to change it
    created_at = serializers.DateTimeField(read_only=True)
 
    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "owner", "created_at"]
 
    # Custom validation — runs when is_valid() is called
    def validate_title(self, value):
        # Title must be at least 3 characters
        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must be at least 3 characters long."
            )
        return value
 
    def validate_status(self, value):
        # Status must be one of the allowed values
        allowed = ["open", "in-progress", "done"]
        if value not in allowed:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(allowed)}"
            )
        return value