from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import User, Blog, Comment, Notification
from .forms import RegisterForm, LoginForm, ChangePasswordForm, ResetPasswordForm, PasswordSetForm,\
					ChangePhotoForm, ChangeInfoForm, PostBlogForm
from .utils import get_cur_page, mark_notification_as_read
# Create your views here.
import re
import json

from .notifications import follow_sig, unfollow_sig, comment_sig
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import detail_route
from rest_framework import renderers
from rest_framework.response import Response
from .serializers import NotificationSerializer

def register(request):
	redirect_to = request.POST.get('next', request.GET.get('next', ''))
	title = 'register'
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.instance.nickname = form.cleaned_data['username']
			form.save()
			login(request, form.instance)
			messages.success(request, 'Welcome to the bIo9 world.')
			if redirect_to:
				return redirect(redirect_to)
			else:
				return redirect(reverse('bIo9:show_user_page', kwargs={'user_id': request.user.id}))
		else:
			return render(request, 'bIo9/register.html', {'form': form, 'title': title})
	else:
		form = RegisterForm()
		return render(request, 'bIo9/register.html', {'form': form, 'title': title})


def index(request):
	blogs = Blog.objects.order_by('-update_time')
	blogs_per_page = 3
	cur_page_no = request.GET.get('page', 1)
	cur_page = get_cur_page(blogs, blogs_per_page, cur_page_no)

	active_users = User.objects.order_by('-last_login')[0:12]
	return render(request, 'bIo9/index.html', {'title': 'index',
												'cur_page': cur_page,
												'users': active_users})


def log_in(request):
	redirect_to = request.POST.get('next', request.GET.get('next', ''))
	title = 'log in'
	if request.method == 'POST':
		form = LoginForm(data=request.POST)
		# import pdb;pdb.set_trace()
		if form.is_valid():
			login(request, form.user_cache)
			messages.success(request, 'You have logged in succesfully.')
			if redirect_to:
				return redirect(redirect_to)
			else:
				return redirect(reverse('bIo9:show_user_page', kwargs={'user_id': request.user.id}))
		else:
			messages.error(request, 'Log in failed.')
			return render(request, 'bIo9/login.html', {'form': form, 'title': title})
	else:
		form = LoginForm()
		return render(request, 'bIo9/login.html', {'form': form, 'title': title, 'next': redirect_to})


@login_required
def log_out(request):
	# import pdb;pdb.set_trace()
	logout(request)
	messages.success(request, 'You have succesfully logged out.')
	redirect_to = request.POST.get('next', request.GET.get('next', ''))
	if redirect_to:
		return redirect(redirect_to)
	else:
		return redirect(reverse('bIo9:index'))
	return redirect('/')


#changing password would logout, let user choose whether to log automatically.
@login_required
def change_password(request):
	title = 'change password'
	if request.method == 'POST':
		form = ChangePasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'password succesfully changed.')
			return redirect(reverse('bIo9:index'))
		else:
			messages.error(request, 'change password failed.')
			return render(request, 'bIo9/change_password.html', {'form': form, 'title': title})
	else:
		form = ChangePasswordForm(request.user)
		return render(request, 'bIo9/change_password.html', {'form': form, 'title': title})


@login_required
def reset_password(request):
	email = request.user.email
	if email == '':
		messages.error(request, "You don't have an email, Please set your email first.")
		return redirect(reverse('bIo9:index'))
	title = 'reset password'
	if request.method == 'POST':
		form = ResetPasswordForm(request.POST)
		if form.is_valid():
			if email == form.cleaned_data['email']:
				form.save(request=request)
				return render(request, 'bIo9/email_sent.html')
			else:
				form.add_error('email', 'the email input does not match your email.')
				return render(request, 'bIo9/reset_password.html', {'form': form, 'title': title})	
		else:
			return render(request, 'bIo9/reset_password.html', {'form': form, 'title': title})
	else:
		form = ResetPasswordForm()
		return render(request, 'bIo9/reset_password.html', {'form': form, 'title': title})


@login_required
@require_POST
def set_new_password(request):
	form = PasswordSetForm(request.user, request.POST)
	if form.is_valid():
		form.save()
		messages.success(request, 'Password succesfully reset.Please log in again.')
		return redirect(reverse('bIo9:index'))
	else:
		messages.error(request, 'Password reset failed.')
		return render(request, 'bIo9/set_new_password.html', {'form': form, 'title': 'set new password'})	


def show_user_page(request, user_id):
	title = 'user page'
	user = get_object_or_404(User, id=user_id)
	blogs = user.blog_set.order_by('-update_time')
	blogs_per_page = 2
	cur_page_no = request.GET.get('page', 1)
	cur_page = get_cur_page(blogs, blogs_per_page, cur_page_no)

	request_user = request.user
	can_follow_user = True
	if request_user.is_authenticated:
		my_follows = request_user.follows.split(';')  
		if str(user.id) in my_follows:
			can_follow_user = False
	else:
		can_follow_user = False

	user_follow_ids = user.follows.split(';')
	user_follows = [ get_object_or_404(User, id=int(x)) for x in user_follow_ids if x != '']
	mark_notification_as_read(request)
	return render(request, 'bIo9/user_page.html', {'cur_user': user, 
													'title': title, 
													'cur_page': cur_page,
													'can_follow_user': can_follow_user,
													'user_follows': user_follows})


@login_required
def change_user_photo(request):
	title = 'change user photo'
	if request.method == 'POST':
		form = ChangePhotoForm(request.POST, request.FILES)
		if request.FILES and form.is_valid():
			photo = form.cleaned_data['photo']
			user = request.user
			if re.match(r'^/media/[1-9]+[0-9]*/.+$', user.photo.url):
				user.photo.delete()
			user.photo = photo
			user.save()
			messages.success(request, 'photo succesfully upload')
			return redirect(reverse('bIo9:show_user_page', kwargs={'user_id': user.id}))
		else:
			if not request.FILES:
				messages.error(request, 'Please choose a file.')
			else:
				messages.error(request, 'upload photo failed')
			return render(request, 'bIo9/change_photo.html', {'form': form, 'title': title})
	else:
		form = ChangePhotoForm()
		return render(request, 'bIo9/change_photo.html', {'form': form, 'title': title})

@login_required
def change_user_info(request):
	cur_user = request.user
	title = 'change user information'
	if request.method == 'POST':
		form = ChangeInfoForm(request.POST)
		if form.is_valid():
			cur_user.nickname = form.cleaned_data['nickname']
			cur_user.age = form.cleaned_data['age']
			cur_user.sex = form.cleaned_data['sex']
			cur_user.email = form.cleaned_data['email']
			cur_user.mood = form.cleaned_data['mood']
			cur_user.introduction = form.cleaned_data['introduction']
			cur_user.save()
			messages.success(request, 'Change Information Done.')
			return redirect(reverse('bIo9:change_user_info'))
		else:
			messages.error(request, 'Change Information Failed.')
			return render(request, 'bIo9/change_user_info.html', {'form': form, 'title': title})
	else:
		form = ChangeInfoForm(cur_user._wrapped.__dict__)
		return render(request, 'bIo9/change_user_info.html', {'form': form, 'title': title})


@login_required
def post_a_blog(request):
	title = 'post a blog'
	if request.method == 'POST':
		form = PostBlogForm(request.POST)
		if form.is_valid():
			request.user.blog_set.create(content=form.cleaned_data['content'])
			return redirect(reverse('bIo9:show_user_page', kwargs={'user_id': request.user.id}))
		else:
			return render(request, 'bIo9/post_a_blog.html', {'form': form, 'title': title})
	else:
		form = PostBlogForm()
		return render(request, 'bIo9/post_a_blog.html', {'form': form, 'title': title})


@login_required
@require_POST
def like_a_blog(request):
	ret_data = {}
	blog_id = int(request.POST['ele_id'].split('_')[-1])
	blog = get_object_or_404(Blog, id=blog_id)
	user_id = request.POST['user_id']
	blog.followers += user_id + ';'
	blog.followers_amt += 1
	blog.save()
	ret_data['result'] = 'success'
	ret_data['new_val'] = blog.followers_amt
	return HttpResponse(json.dumps(ret_data))


@login_required
@require_POST
def follow_a_user(request):
	ret_data = {}
	user = request.user
	followee_id = request.POST['page_user_id']
	user.follows += followee_id + ';'
	user.save()
	ret_data['result'] = 'success'	
	follow_sig.send(user.__class__, follower=user.id, followee=followee_id)
	return HttpResponse(json.dumps(ret_data))

@login_required
@require_POST
def unfollow_a_user(request):
	ret_data = {}
	user = request.user
	follows_list = user.follows.split(';')
	followee_id = request.POST['page_user_id']
	follows_list.remove(followee_id)
	user.follows = ';'.join(follows_list) if len(follows_list) != 0 else ''
	user.save()
	ret_data['result'] = 'success'
	unfollow_sig.send(user.__class__, follower=user.id, followee=followee_id)
	return HttpResponse(json.dumps(ret_data))

class NotificationListView(LoginRequiredMixin, ListView):
	model = Notification
	context_object_name = 'notifications'
	template_name = 'bIo9/notification_list.html'
	login_url = reverse_lazy('bIo9:login')

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(note_obj=self.request.user)


def make_a_comment(request, blog_id):
	title = 'comment'
	blog = get_object_or_404(Blog, id=blog_id)
	if request.method == 'POST':
		if request.user.is_authenticated:
			content = request.POST['content']
			reply_to = request.POST.get('reply_to', None)
			my_floor = blog.comment_set.count() + 1
			comment = blog.comment_set.create(user=request.user, content=content, reply_to_id=reply_to, my_floor=my_floor)
			comment.save()
			redirect_to = request.POST['next']
			if reply_to and reply_to != request.user.id :
				comment = get_object_or_404(Comment, id=reply_to)
				comment_sig.send(Comment, commenter=request.user.id, commentee=comment.user.id, blog=blog, comment=comment)
			else:
				if request.user != blog.user:
					comment_sig.send(Comment, commenter=request.user.id, commentee=blog.user.id, blog=blog, comment=None)
			mark_notification_as_read(request)
			return redirect(redirect_to)
		else:
			messages.error(request, 'Please log in first.')
			return redirect('bIo9:index')
	else:
		comments = blog.comment_set.order_by('-create_time')
		page_no = request.GET.get('page')
		comment_per_page = 2
		cur_page = get_cur_page(comments, comment_per_page, page_no)
		mark_notification_as_read(request)
		return render(request, 'bIo9/make_a_comment.html', {'title': title, 'cur_page': cur_page, 'obj': blog})


@require_GET
def get_full_chat(request, comment_id):
	title = 'full chat'
	cur_comment = Comment.objects.get(pk=comment_id)
	full_chat = [cur_comment]
	if cur_comment.reply_to:
		full_chat.insert(0, cur_comment.reply_to)
	replys = cur_comment.comment_set.all()
	full_chat += replys
	comment_per_page = 3
	page_no = request.GET.get('page', None)
	cur_page = get_cur_page(full_chat, comment_per_page, page_no)
	mark_notification_as_read(request)
	return render(request, 'bIo9/full_chat.html', {'title': title, 'cur_page': cur_page})


class NotificationListApiView(LoginRequiredMixin, ReadOnlyModelViewSet):
	serializer_class = NotificationSerializer
	queryset = Notification.objects.filter(has_read=False)
	login_url = reverse_lazy('bIo9:login')

	def get_queryset(self):
		queryset = super().get_queryset().filter(note_obj=self.request.user)
		return queryset
	
	@detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
	def count(self, request, *args, **kwargs):
		# import pdb; pdb.set_trace()
		return Response({'count': self.get_queryset().count()})

class NotificationUpdateApiView(LoginRequiredMixin, ModelViewSet):
	serializer_class = NotificationSerializer
	login_url = reverse_lazy('bIo9:login')
	queryset = Notification.objects.all()

	def get_queryset(self):
		queryset = super().get_queryset().filter(note_obj=self.request.user)
		return queryset
	

