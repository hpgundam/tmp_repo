from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




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

