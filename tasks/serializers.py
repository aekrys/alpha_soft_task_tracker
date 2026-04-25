from rest_framework import serializers
from .models import Project, Task, Comment



class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]


    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["created_by"] = request.user

        participants = validated_data.get("participants", [])
        if request.user not in participants:
            participants.append(request.user)
            validated_data["participants"] = participants

        return super().create(validated_data)



class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["creator", "created_at", "updated_at"]


    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["creator"] = request.user
        validated_data["status"] = "new"

        return super().create(validated_data)


    def validate(self, data):
        request = self.context.get("request")

        if "executor" in data and data["executor"]:
            if self.instance:
                project = self.instance.project
            else:
                project = data.get("project")

            if project and not project.participants.filter(id=data["executor"].id).exists():
                raise serializers.ValidationError({
                    "executor": "Исполнитель должен быть участником проекта."
                })

        if self.instance and request:
            user = request.user
            instance = self.instance

            is_owner = (instance.project.created_by == user)
            is_creator = (instance.creator == user)
            is_executor = (instance.executor == user)

            if is_owner:
                return data

            if is_creator and not is_owner:
                allowed_fields = ["description"]
                for field in data.keys():
                    if field not in allowed_fields:
                        raise serializers.ValidationError({
                            "field": "Нет прав для изменения данного поля."
                        })

            if is_executor and not is_owner and not is_creator:
                allowed_fields = ["status", "priority"]
                for field in data.keys():
                    if field not in allowed_fields:
                        raise serializers.ValidationError({
                            "field": "Нет прав для изменения данного поля."
                        })

            if not (is_owner or is_creator or is_executor):
                raise serializers.ValidationError({
                    "task": "Нет прав на редактирование данной задачи."
                })

        return data



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author", "created_at"]


    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)


    def validate(self, data):
        request = self.context.get("request")
        if not request:
            return data

        user = request.user

        if self.instance:
            task = self.instance.task
        else:
            task = data.get("task")

        if not task:
            raise serializers.ValidationError({
                "task": "Необходимо указать задачу."
            })

        is_owner = (task.project.created_by == user)
        is_creator = (task.creator == user)
        is_executor = (task.executor == user)
        is_participant = (task.project.participants.filter(id=user.id).exists())

        if not (is_owner or is_creator or is_executor or is_participant):
            raise serializers.ValidationError({
                "task": "Нет доступа к данной задаче."
            })

        if self.instance and self.instance.author != user:
            raise serializers.ValidationError({
                "comment": "Нет возможности изменять комментарии других пользователей."
            })

        return data