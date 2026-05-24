from django.contrib import admin
from .models import Profile, Complaint, ComplaintComment, ComplaintHistory


admin.site.register(Profile)
admin.site.register(Complaint)
admin.site.register(ComplaintComment)
admin.site.register(ComplaintHistory)
