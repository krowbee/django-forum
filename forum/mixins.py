from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import Profile
from django.core.exceptions import PermissionDenied


class ProfileAndLoginRequired(LoginRequiredMixin):
    login_url = '/accounts/login'

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
        try:
            profile_exists = bool(request.user.profile)
        except Profile.DoesNotExist:
            profile_exists = False

        if request.path == reverse('create-profile'):
            if profile_exists:
                return redirect('homepage')
            else:
                return super().dispatch(request, *args, **kwargs)

        if profile_exists:
            return super().dispatch(request, *args, **kwargs)

        return redirect('create-profile')


class AuthorOrSuperuserPermissionMixin:

    model = None

    id_url_kwarg = 'id'

    permission_message = "У вас немає прав доступа до цього об'єкту"

    def get_object(self):
        if not self.model:
            raise "Model is not specified in the mixin or the view."

        obj = get_object_or_404(self.model, id=self.kwargs.get(self.id_url_kwarg))
        if not (obj.author == self.request.user or self.request.user.is_superuser):
            raise PermissionDenied(self.permission_message)
        return obj
