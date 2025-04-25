from rest_framework import serializers


class DemoFlagSerializer(serializers.Serializer):
    def save(self, **kwargs):
        instance = super().save(**kwargs)

        request = self.context.get('request')
        print('Вызываем save')
        if getattr(request.user, 'is_demo', False):
            print('Попали в условие, оно выполнилось')
            instance.is_demo = True
            instance.save(update_fields=['is_demo'])

        print('instance =', instance)

        return instance


class DemoFlagModelSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        instance = super().save(**kwargs)

        request = self.context.get('request')
        if getattr(request.user, 'is_demo', False):
            instance.is_demo = True
            instance.save(update_fields=['is_demo'])

        return instance
