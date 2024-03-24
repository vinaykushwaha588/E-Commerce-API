from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, mobile, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError("Email id required!")
        if not mobile:
            raise ValueError("Mobile number is required!")

        email = self.normalize_email(email)
        user = self.model(email=email, mobile=mobile, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, mobile, first_name=None, last_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_inactive', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True!')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True!')

        return self.create_user(email, password, mobile, first_name, last_name, **extra_fields)
