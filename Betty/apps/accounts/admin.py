from django.contrib import admin as django_admin
from django.contrib.auth import admin, get_user_model
from django.contrib.auth.admin import UserChangeForm, UserCreationForm
from django.contrib.auth.forms import AdminPasswordChangeForm

User = get_user_model()


class UserAdmin(admin.UserAdmin):
    fieldsets = (
        ('Account Information', {
            'fields': (
                'username',
                'password',
                'email',
                'balance'
            ),
        }),
        ('Personal Information', {
            'fields': (
                'first_name',
                'last_name',
                'birth_date',
                'country'
            )

        }),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = (
        'username', 'email', 'first_name', 'last_name'
    )

    search_fields = ('email', 'first_name', 'last_name', 'username')


django_admin.site.register(User, UserAdmin)
