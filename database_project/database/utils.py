user_unauthorized_items = [{'title': 'Регистрация', 'url_name': 'accounts-register'},
                           {'title': 'Войти', 'url_name': 'accounts-login'}]
user_authorized_items = [{'title': 'Профиль', 'url_name': 'accounts-home'},
                         {'title': 'Выход', 'url_name': 'accounts-logout'}]


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['user_items'] = user_unauthorized_items if not self.request.user.is_authenticated \
            else user_authorized_items

        return context
