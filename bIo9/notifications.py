from .models import User, Notification
from django.dispatch import Signal




def follow_notification(sender, follower, followee, **kwargs):
    Notification.objects.create(note_sub_id=follower, note_obj_id=followee, note_verb='followed')

follow_sig = Signal(providing_args=['follower', 'followee'])
follow_sig.connect(follow_notification)

def unfollow_notification(sender, follower, followee, **kwargs):
    Notification.objects.create(note_sub_id=follower, note_obj_id=followee, note_verb='unfollowed')

unfollow_sig = Signal(providing_args=['follower', 'followee'])
unfollow_sig.connect(unfollow_notification)

def comment_notification(sender, commenter, commentee, blog, comment, **kwargs):
    Notification.objects.create(note_sub_id=commenter, note_obj_id=commentee, blog=blog, comment=comment, note_verb='commented')

comment_sig = Signal(providing_args=['commenter', 'commentee', 'blog', 'comment'])
comment_sig.connect(comment_notification)
