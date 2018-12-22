import datetime

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from .models import Action


def create_action(user, verb, target=None):
    """
        Initial code
            action = Action(user=user, verb=verb, target=target)
            action.save()
            
        actual usage (e.g. avoiding dup actions in the activity stream)
            when u "like -> unlike -> like -> unlike" an image,
            the actual opt should only ONE (aka like -> unlike) instead 4 actions!
    """
    
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    
    # Multiple actions (which gen same result)
    #   that happened during <last min -> now> will be combined as ONE action
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute)
    
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        
        # (false | save)
        #   if the opt was NOT done during the last min till now
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                 target_id=target.id)
    
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        
        # create action (lol)
        return True
    
    return False