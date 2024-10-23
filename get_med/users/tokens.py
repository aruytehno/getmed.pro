from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Используем str() вместо six.text_type
        return str(user.pk) + str(timestamp) + str(user.is_active)

email_confirmation_token = EmailConfirmationTokenGenerator()
