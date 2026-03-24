from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q


class EmailAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in
    using either their email address OR their username.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the user exists by looking up the username OR the email
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            return None

        # If the user exists, verify the password
        if user.check_password(password) and self.user_can_authenticate(user):
            return user