from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    """
        The `for_fields` is an optional param that
            | allows us to indicated the fields
            | that the order has be calc_ed with respect to
            
        We're also overriding the `pre_save` (inherited from parent class)
            Note: any code that you're not familiar with is cuz_ed by parent class.
        
        _
    """
    
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)
        
    def pre_save(self, model_instance, add):
        
        if getattr(model_instance, self.attname) is None:
            
            try:
                # retrieve all objs for the field's model
                qset = self.model.objects.all()
                
                if self.for_fields:
                    
                    # filter by objs with the same field vals
                    # for the fields in `for_fields`
                    query   = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    
                    qset    = qset.filter(**query)
                
                # get the order of the last item
                last_item   = qset.latest(self.attname)
                value       = last_item.order + 1
                
            except ObjectDoesNotExist:
                value       = 0
            
            setattr(model_instance, self.attname, value)
            
            return value
        
        else:
            # We won't do anything for the `else` case
            return super(OrderField,
                         self).pre_save(model_instance, add)