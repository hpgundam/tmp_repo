from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.forms import ModelForm, Textarea, HiddenInput
from .models import User, Blog


class RegisterForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User


class LoginForm(AuthenticationForm):
	class Meta:
		model = User


class ChangePasswordForm(PasswordChangeForm):
	class Meta:
		model = User


class ResetPasswordForm(PasswordResetForm):
	class Meta:
		model = User

	def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='bIo9/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
		super(ResetPasswordForm, self).save(domain_override=domain_override,
             subject_template_name=subject_template_name,
             email_template_name=email_template_name,
             use_https=use_https, token_generator=token_generator,
             from_email=from_email, request=request, html_email_template_name=html_email_template_name,
             extra_email_context=extra_email_context)


class PasswordSetForm(SetPasswordForm):
	class Meta:
		model = User


class ChangePhotoForm(ModelForm):
	class Meta:
		model = User
		fields = ('photo',)


class ChangeInfoForm(ModelForm):
	class Meta:
		model = User
		fields = ('nickname', 'age', 'sex', 'email', 'mood', 'introduction')
		widgets = {
		'mood': Textarea(attrs={'rows': 1}),
		'introduction': Textarea(attrs={'rows': 2})
		}

class PostBlogForm(ModelForm):
	class Meta:
		model = Blog
		fields = ('content',)
		widgets = {
		'content': Textarea(attrs={'rows': 2, 'placeholder': 'blog content ...', 'required': 'required'}),
		}










