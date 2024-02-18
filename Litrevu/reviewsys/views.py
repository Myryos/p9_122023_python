from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from django.db.models import CharField, Value
from .queries import (
    get_users_viewable_reviews,
    get_users_viewable_tickets,
    get_followers_user,
    get_following_user,
    get_users_by_string,
)

from .models import Ticket, Review, UserFollows
from authentication.models import User

from .forms import TicketForm, ReviewForm


from django.http import JsonResponse, HttpResponseForbidden

from django.core.exceptions import ValidationError


@login_required
def flow(request):
    user = request.user

    reviews = Review.objects.all()
    reviews = reviews.annotate(content_types=Value("REVIEW", CharField()))

    tickets = Ticket.objects.all()
    tickets = tickets.annotate(content_types=Value("TICKET", CharField()))

    for review in reviews:
        review.ticket = Ticket.objects.get(pk=review.ticket_id)
        print(review.ticket)

    post = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    return render(
        request, "home/home.html", context={"posts": post, "user": request.user}
    )


@login_required
def posts(request):
    user = request.user

    if user is None:
        return redirect("login")
    reviews = get_users_viewable_reviews(user)
    reviews = reviews.annotate(content_types=Value("REVIEW", CharField()))

    tickets = get_users_viewable_tickets(user)
    tickets = tickets.annotate(content_types=Value("TICKET", CharField()))

    post = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    return render(request, "post.html", context={"posts": post})


@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)

            ticket.user = request.user
            ticket.save()
            return redirect("home")
    else:
        form = TicketForm()
    return render(request, "forms/ticket_form.html", {"form": form})


@login_required
def ticket_update(request, ticket_id):
    message = ""
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.user != request.user:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à effectuer cette action."
        )
    form = TicketForm(instance=ticket)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        print(request.FILES)
        if form.is_valid():
            print("form is valid")
            form.save()
            return redirect("home")
        else:
            message = "Erreur dans le formulaire"
    return render(
        request, "forms/ticket_update.html", {"form": form, "message": message}
    )


@login_required
def ticket_delete(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if ticket.user != request.user:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à effectuer cette action."
        )

    if request.method == "POST":
        ticket.delete()
        return redirect("posts")

    return render(request, "forms/delete_ticket_form.html")


@login_required
def review_create(request, ticket_id):
    form = ReviewForm()
    form.ticket = Ticket.objects.get(id=ticket_id)
    existing_review = Review.objects.filter(ticket=ticket_id).exists()

    if existing_review is True:
        raise ValidationError("Une revue existe déjà pour ce ticket.")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.ticket_id = ticket_id
            review.user = request.user
            review.save()
            return redirect("home")
    return render(request, "forms/review_form.html", {"form": form})


@login_required
def review_update(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    form = ReviewForm(instance=review)
    form.ticket = Ticket.objects.get(id=review.ticket_id)

    if review.user != request.user:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à effectuer cette action."
        )

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("home")
    return render(request, "forms/review_update.html", {"form": form})


@login_required
def review_delete(request, review_id):
    review = Review.objects.get(id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden(
            "Vous n'êtes pas autorisé à effectuer cette action."
        )

    if request.method == "POST":
        review.delete()
        return redirect("posts")

    return render(request, "forms/delete_review_form.html")


@login_required
def ticket_review_create(request):

    ticketForm = TicketForm()
    reviewForm = ReviewForm()
    savedTicket = False
    savedReview = False
    if request.method == "POST":

        ticketForm = TicketForm(request.POST)

        if ticketForm.is_valid():
            ticket = ticketForm.save(commit=False)

            ticket.user = request.user

            ticket.save()
            savedTicket = True
        reviewForm = ReviewForm(request.POST)
        if reviewForm.is_valid():
            review = reviewForm.save(commit=False)
            review.ticket_id = ticket.id
            review.user = request.user
            review.save()
            savedReview = True
        if savedTicket and savedReview:
            redirect("home")
    return render(
        request,
        "forms/tikect_review_form.html",
        {"formTicket": ticketForm, "formReview": reviewForm},
    )


@login_required
def abonnements_view(request):

    followers_list = get_followers_user(request.user)

    following_list = get_following_user(request.user)
    return render(
        request,
        "abonnements.html",
        {"followers": followers_list, "followed": following_list},
    )


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, name=username)
    if user_to_follow != request.user:
        UserFollows.objects.get_or_create(
            user=request.user, followed_user=user_to_follow
        )
        return redirect("abonnements")


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, name=username)

    if user_to_unfollow != request.user:
        UserFollows.objects.filter(
            user=request.user, followed_user=user_to_unfollow
        ).delete()

    return redirect("abonnements")


@login_required
def search_not_followed_user(request, input_string):

    users_names = get_users_by_string(input_string, request.user.id)

    data = [{"name": user_name} for user_name in users_names]

    return JsonResponse(data=data, safe=False)
