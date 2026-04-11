import json

from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext as _

from .models import Conversation, Message


@login_required
def conversation_list_view(request):
    employer_convs = Conversation.objects.filter(employer=request.user).select_related('job', 'worker', 'worker__profile')
    worker_convs = Conversation.objects.filter(worker=request.user).select_related('job', 'employer', 'employer__profile')
    conversations = list(employer_convs) + list(worker_convs)
    conversations.sort(key=lambda c: c.created_at, reverse=True)

    if conversations:
        ids = [c.pk for c in conversations]
        rows = (
            Message.objects.filter(conversation_id__in=ids, is_read=False)
            .exclude(sender=request.user)
            .values('conversation_id')
            .annotate(total=Count('id'))
        )
        unread_map = {row['conversation_id']: row['total'] for row in rows}
        for c in conversations:
            c.unread_for_user = unread_map.get(c.pk, 0)

    return render(request, 'chat/conversation_list.html', {'conversations': conversations})


@login_required
def conversation_detail_view(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in [conversation.employer, conversation.worker]:
        return redirect('conversation_list')

    conversation.messages.exclude(sender=request.user).update(is_read=True)

    messages_qs = conversation.messages.select_related('sender').all()
    return render(request, 'chat/conversation_detail.html', {
        'conversation': conversation,
        'chat_messages': messages_qs,
    })


@login_required
def send_message_view(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in [conversation.employer, conversation.worker]:
        return JsonResponse({'error': _('Permission denied.')}, status=403)

    if request.method != 'POST':
        return JsonResponse({'error': _('Invalid request.')}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': _('Invalid JSON.')}, status=400)

    body = data.get('body', '').strip()
    if body:
        msg = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            body=body
        )
        return JsonResponse({
            'id': msg.pk,
            'body': msg.body,
            'sender': request.user.get_full_name() or request.user.username,
            'sender_id': request.user.pk,
            'timestamp': msg.timestamp.strftime('%H:%M'),
            'is_own': True,
        })
    return JsonResponse({'error': _('Invalid request.')}, status=400)


@login_required
def get_messages_view(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if request.user not in [conversation.employer, conversation.worker]:
        return JsonResponse({'error': _('Permission denied.')}, status=403)

    after_id = request.GET.get('after', 0)
    messages_qs = conversation.messages.filter(pk__gt=after_id).select_related('sender')
    messages_qs.exclude(sender=request.user).update(is_read=True)

    data = [{
        'id': m.pk,
        'body': m.body,
        'sender': m.sender.get_full_name() or m.sender.username,
        'sender_id': m.sender.pk,
        'timestamp': m.timestamp.strftime('%H:%M'),
        'is_own': m.sender == request.user,
    } for m in messages_qs]

    return JsonResponse({'messages': data})
