from inventory.models import Notifications

def notifications_context(request):
    notifications = Notifications.objects.filter(status=True).order_by('status')[:5]
    return {'notifications': notifications}