from chat.models import Conversation, Message
from django.db.models import Q


def site_preferences(request):
    """Theme from profile (light/dark); default light."""
    theme = 'light'
    if request.user.is_authenticated:
        try:
            theme = request.user.profile.theme_preference or 'light'
        except Exception:
            theme = 'light'
    return {'user_theme': theme}


def unread_notifications(request):
    """Add unread message count to every page context."""
    if not request.user.is_authenticated:
        return {'unread_count': 0}

    try:
        # Get all conversations where user is employer OR worker (single query, no UNION)
        conversations = Conversation.objects.filter(
            Q(employer=request.user) | Q(worker=request.user)
        ).values_list('id', flat=True)

        unread = Message.objects.filter(
            conversation_id__in=list(conversations),
            is_read=False
        ).exclude(sender=request.user).count()

        return {'unread_count': unread}
    except Exception:
        return {'unread_count': 0}
