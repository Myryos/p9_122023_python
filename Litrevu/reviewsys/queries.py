from .models import Review, Ticket, UserFollows
from authentication.models import User


def get_users_viewable_reviews(user):
    users_viewable_reviews = Review.objects.filter(user=user)
    return users_viewable_reviews


def get_users_viewable_tickets(user):
    users_viewable_tickets = Ticket.objects.filter(user=user)
    return users_viewable_tickets


def get_following_user(user):
    following_ids = UserFollows.objects.filter(user=user).values("followed_user")

    following_list = User.objects.filter(id__in=following_ids)
    return following_list


def get_followers_user(user):
    followers_list = UserFollows.objects.filter(followed_user=user.id)

    return followers_list


def get_users_by_string(searched_user, user):
    users = User.objects.filter(name__icontains=searched_user).exclude(id=user)
    following_user = UserFollows.objects.filter(user=user).values_list(
        "followed_user", flat=True
    )
    users_names = users.exclude(id__in=following_user).values_list("name", flat=True)
    return sorted(users_names)
