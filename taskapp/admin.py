from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from simple_history.admin import SimpleHistoryAdmin

from taskapp.models import Staff, Project, Task


# Define an inline admin descriptor for Staff model
# which acts a bit like a singleton
class StaffInline(admin.StackedInline):
    model = Staff
    can_delete = False
    verbose_name_plural = 'staff'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (StaffInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Project, SimpleHistoryAdmin)
admin.site.register(Task, SimpleHistoryAdmin)