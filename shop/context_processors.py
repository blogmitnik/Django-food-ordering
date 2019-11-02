from .models import Category, Place, Product
from like.models import Like

def menu_links(request):
	links = Category.objects.all()
	return dict(links=links)

def place_list(request):
	place_list = Place.objects.all()
	return dict(place_list=place_list)

def liked_by_user(request):
	if request.user.is_authenticated:
		liked_items = Like.objects.filter(user_id=request.user.id)
		liked_items_pids = [liked_item.product_id for liked_item in liked_items]
		return dict(liked_items=liked_items_pids)
	else:
		return {}