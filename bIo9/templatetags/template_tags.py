from django import template
from ..models import Blog

register = template.Library()

@register.filter
def blog_can_be_followed(blog, user_id):
	return blog.can_be_followed_by(user_id)

