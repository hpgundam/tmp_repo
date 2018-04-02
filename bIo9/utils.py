from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bIo9.models import Notification
from django.shortcuts import get_object_or_404


def get_cur_page(objs, obj_amt_per_page, cur_page):
	paginator = Paginator(objs, obj_amt_per_page)
	try:
		page = paginator.page(cur_page)
	except (EmptyPage, PageNotAnInteger):
		page = paginator.page(1)
	return page


def user_factory(counter):
	users = {}
	for i in range(counter):
		username = 'user%d' % i
		users[username] = 'hp123123'
	return users

def mark_notification_as_read(request):
	notification_id = request.GET.get('notification_id', None)
	if notification_id is not None:
		notification = get_object_or_404(Notification, id=notification_id)
		notification.has_read = True
		notification.save()

