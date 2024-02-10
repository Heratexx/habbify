from .models import ExperiencePoint, Level
from django.db.models import Sum

def profile_info(request):
    if(request.user.id):
        user = request.user
        total_xp = ExperiencePoint.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        user_level = calculate_user_level(total_xp)
        return {'user_level': user_level, 'total_xp': total_xp}
    else:
        return {}

def calculate_user_level(total_xp):
    levels = Level.objects.all().order_by('level_number')
    user_level = 1
    for level in levels:
        if total_xp >= level.xp_threshold:
            user_level = level.level_number
        else:
            break
    return user_level