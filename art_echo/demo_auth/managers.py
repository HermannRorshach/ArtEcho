class DemoQuerySetManager:
    def __init__(self, model_cls):
        self.model_cls = model_cls

    def for_user(self, user):
        qs = self.model_cls.objects.all()
        if getattr(user, 'is_demo', False):
            return qs.filter(is_demo=True)
        return qs.exclude(is_demo=True)
