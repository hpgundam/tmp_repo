from django.conf.urls import url
from django.contrib.auth.views import password_reset_confirm
from .views import register, index, log_in, log_out, change_password, reset_password, set_new_password,\
					show_user_page, change_user_photo, change_user_info, post_a_blog, like_a_blog,\
					follow_a_user, make_a_comment, get_full_chat

app_name = 'bIo9'

urlpatterns = [
	url(r'^$', index, name='index'),
	#authentication
	url(r'^register/$', register, name='register'),
	url(r'^login/$', log_in, name='login'),
	url(r'^logout/$', log_out, name='logout'),
	url(r'^change_password/$', change_password, name="change_password"),
	url(r'^reset_password/$', reset_password, name="reset_password"),
	url(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'post_reset_redirect': 'bIo9:set_new_password', 'template_name': 'bIo9/set_new_password.html'}, name="password_reset_confirm"),
	url(r'^reset_password/set_new_password$', set_new_password, name='set_new_password'),
	#user
	url(r'^user/user_id=(?P<user_id>[1-9]+[0-9]*)/$', show_user_page, name='show_user_page'),
	url(r'^user/change_photo$', change_user_photo, name='change_user_photo'),
	url(r'^user/change_info$', change_user_info, name='change_user_info'),
	url(r'^user/post_a_blog$', post_a_blog, name='post_a_blog'),
	url(r'^user/like_a_blog$', like_a_blog, name='like_a_blog'),
	url(r'^user/follow_a_user$', follow_a_user, name='follow_a_user'),
	url(r'^user/comment/blog_id=(?P<blog_id>[1-9]+[0-9]*)$', make_a_comment, name='make_a_comment'),
	url(r'^user/comment/comment_id=(?P<comment_id>[1-9]+[0-9]*)$', get_full_chat, name='get_full_chat'),
]

