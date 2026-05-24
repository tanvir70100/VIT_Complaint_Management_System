from urllib import request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Complaint, ComplaintHistory
from .forms import ComplaintForm, CommentForm, VerdictForm, ComplaintEditForm
from .services import assign_reviewer


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = AuthenticationForm()

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username:
            messages.error(request, "Username is required.")
            return render(request, 'complaints/login.html', {'form': form})

        if not password:
            messages.error(request, "Password is required.")
            return render(request, 'complaints/login.html', {'form': form})

        user_exists = User.objects.filter(username=username).exists()

        if not user_exists:
            messages.error(request, "No account found with this username.")
            return render(request, 'complaints/login.html', {'form': form})

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Password is incorrect. Please try again.")
            return render(request, 'complaints/login.html', {'form': form})

        if not user.is_active:
            messages.error(request, "This account is inactive. Please contact the administrator.")
            return render(request, 'complaints/login.html', {'form': form})

        login(request, user)
        messages.success(request, "Login successful.")
        return redirect('dashboard')

    return render(request, 'complaints/login.html', {'form': form})

def create_complaint_history(complaint, changed_by, action, old_value=None, new_value=None):
    ComplaintHistory.objects.create(
        complaint=complaint,
        changed_by=changed_by,
        action=action,
        old_value=old_value,
        new_value=new_value
    )

@login_required
def dashboard(request):
    user = request.user

    active_count = Complaint.objects.filter(
        Q(complainant=user) | Q(reviewer=user) | Q(accused=user),
        status__in=['active', 'under_review']
    ).count()

    previous_count = Complaint.objects.filter(
        Q(complainant=user) | Q(reviewer=user) | Q(accused=user),
        status__in=['resolved', 'rejected', 'closed']
    ).count()

    reviewer_count = Complaint.objects.filter(
        reviewer=user,
        status__in=['active', 'under_review']
    ).count()

    context = {
        'active_count': active_count,
        'previous_count': previous_count,
        'reviewer_count': reviewer_count,
    }

    return render(request, 'complaints/dashboard.html', context)


@login_required
def lodge_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(
            request.POST,
            request.FILES,
            current_user=request.user
        )

        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.complainant = request.user

            try:
                complaint.reviewer = assign_reviewer(complaint.accused)
                complaint.save()

                create_complaint_history(
                    complaint=complaint,
                    changed_by=request.user,
                    action="Complaint lodged",
                    old_value="No complaint existed",
                    new_value=f"Complaint '{complaint.title}' was created"
                )

                messages.success(request, "Complaint lodged successfully. Reviewer has been assigned automatically.")
                return redirect('active_complaints')

            except ValueError as error:
                messages.error(request, str(error))

    else:
        form = ComplaintForm(current_user=request.user)

    return render(request, 'complaints/lodge_complaint.html', {'form': form})


@login_required
def active_complaints(request):
    complaints = Complaint.objects.filter(
        Q(complainant=request.user) |
        Q(reviewer=request.user) |
        Q(accused=request.user),
        status__in=['active', 'under_review']
    ).order_by('-created_at')

    return render(request, 'complaints/complaint_list.html', {
        'complaints': complaints,
        'title': 'Active Complaints'
    })


@login_required
def previous_complaints(request):
    complaints = Complaint.objects.filter(
        Q(complainant=request.user) |
        Q(reviewer=request.user) |
        Q(accused=request.user),
        status__in=['resolved', 'rejected', 'closed']
    ).order_by('-created_at')

    return render(request, 'complaints/complaint_list.html', {
        'complaints': complaints,
        'title': 'Previous Complaints'
    })


@login_required
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    is_allowed = (
        complaint.complainant == request.user or
        complaint.reviewer == request.user or
        complaint.accused == request.user
    )

    if not is_allowed:
        messages.error(request, "You are not allowed to view this complaint.")
        return redirect('dashboard')

    comment_form = CommentForm()
    verdict_form = VerdictForm(instance=complaint)

    if request.method == 'POST':
        if 'add_comment' in request.POST:
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.complaint = complaint
                comment.user = request.user
                comment.save()

                create_complaint_history(
                    complaint=complaint,
                    changed_by=request.user,
                    action="Comment added",
                    old_value="No comment",
                    new_value=comment.comment
                )

                messages.success(request, "Comment added successfully.")
                return redirect('complaint_detail', complaint_id=complaint.id)

        elif 'update_verdict' in request.POST:
            if complaint.reviewer != request.user:
                messages.error(request, "Only the assigned reviewer can update the verdict.")
                return redirect('complaint_detail', complaint_id=complaint.id)

            old_status = complaint.status
            old_verdict = complaint.verdict or "No verdict"

            verdict_form = VerdictForm(request.POST, instance=complaint)

            if verdict_form.is_valid():
                updated_complaint = verdict_form.save()

                if old_status != updated_complaint.status:
                    create_complaint_history(
                        complaint=updated_complaint,
                        changed_by=request.user,
                        action="Status updated",
                        old_value=old_status,
                        new_value=updated_complaint.status
                    )

                new_verdict = updated_complaint.verdict or "No verdict"

                if old_verdict != new_verdict:
                    create_complaint_history(
                        complaint=updated_complaint,
                        changed_by=request.user,
                        action="Verdict updated",
                        old_value=old_verdict,
                        new_value=new_verdict
                    )

                messages.success(request, "Verdict and status updated successfully.")
                return redirect('complaint_detail', complaint_id=complaint.id)

    can_view_history = (
        complaint.complainant == request.user or
        complaint.reviewer == request.user
    )

    can_edit_complaint = (
        complaint.complainant == request.user and
        complaint.status not in ['resolved', 'rejected', 'closed']
    )

    context = {
        'complaint': complaint,
        'comment_form': comment_form,
        'verdict_form': verdict_form,
        'is_reviewer': complaint.reviewer == request.user,
        'is_accused': complaint.accused == request.user,
        'is_complainant': complaint.complainant == request.user,
        'can_view_history': can_view_history,
        'can_edit_complaint': can_edit_complaint,
    }

    return render(request, 'complaints/complaint_detail.html', context)

@login_required
def edit_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if complaint.complainant != request.user:
        messages.error(request, "Only the complainant can edit this complaint.")
        return redirect('complaint_detail', complaint_id=complaint.id)

    if complaint.status in ['resolved', 'rejected', 'closed']:
        messages.error(request, "This complaint cannot be edited because it has already been finalised.")
        return redirect('complaint_detail', complaint_id=complaint.id)

    old_title = complaint.title
    old_description = complaint.description
    old_evidence = complaint.evidence.name if complaint.evidence else "No evidence"

    if request.method == 'POST':
        form = ComplaintEditForm(request.POST, request.FILES, instance=complaint)

        if form.is_valid():
            updated_complaint = form.save()

            changes = []

            if old_title != updated_complaint.title:
                changes.append(
                    f"Title changed from '{old_title}' to '{updated_complaint.title}'"
                )

                create_complaint_history(
                    complaint=updated_complaint,
                    changed_by=request.user,
                    action="Title updated",
                    old_value=old_title,
                    new_value=updated_complaint.title
                )

            if old_description != updated_complaint.description:
                changes.append("Description updated")

                create_complaint_history(
                    complaint=updated_complaint,
                    changed_by=request.user,
                    action="Description updated",
                    old_value=old_description,
                    new_value=updated_complaint.description
                )

            new_evidence = updated_complaint.evidence.name if updated_complaint.evidence else "No evidence"

            if old_evidence != new_evidence:
                changes.append(
                    f"Evidence changed from '{old_evidence}' to '{new_evidence}'"
                )

                create_complaint_history(
                    complaint=updated_complaint,
                    changed_by=request.user,
                    action="Evidence updated",
                    old_value=old_evidence,
                    new_value=new_evidence
                )

            if not changes:
                messages.info(request, "No changes were made to the complaint.")
            else:
                messages.success(request, "Complaint updated successfully.")

            return redirect('complaint_detail', complaint_id=complaint.id)

    else:
        form = ComplaintEditForm(instance=complaint)

    return render(request, 'complaints/edit_complaint.html', {
        'form': form,
        'complaint': complaint
    })