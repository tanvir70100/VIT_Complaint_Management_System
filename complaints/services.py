from django.contrib.auth.models import User
from .models import Profile


def assign_reviewer(accused_user):
    accused_profile = Profile.objects.get(user=accused_user)
    accused_role = accused_profile.role

    hierarchy = {
        'student': 'faculty',
        'faculty': 'unit_coordinator',
        'unit_coordinator': 'admin_director',
        'admin_staff': 'admin_director',
        'admin_director': 'pro_vc',
        'pro_vc': 'vc',
    }

    if accused_role == 'vc':
        raise ValueError("Complaints against the VC are not allowed.")

    reviewer_role = hierarchy.get(accused_role)

    if reviewer_role is None:
        raise ValueError("Reviewer role could not be assigned.")

    reviewer_profile = Profile.objects.filter(role=reviewer_role).first()

    if reviewer_profile is None:
        raise ValueError(f"No reviewer found for role: {reviewer_role}")

    return reviewer_profile.user