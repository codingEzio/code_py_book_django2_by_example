# -*- coding: utf-8 -*-

import redis
from django.conf import settings

from .models import Product

# Making connection
rdb = redis.StrictRedis(host=settings.REDIS_HOST,
                        port=settings.REDIS_PORT,
                        db=settings.REDIS_DB)


class Recommender(object):
    
    def get_product_key(self, id):
        """
            Eventually this func is just for
                generating a key (diff product) for later "recommendation".
            
            e.g.
                product:{0}:purchased_with <val>
                product:{1}:purchased_with <val>
        """
        
        return 'product:{}:purchased_with'.format(id)
    
    def products_bought(self, products):
        """
            The products are what we bought within an order.
        
            Retrieving the products that being bought together
                which belongs to the same order (we ARE getting from it).
            
            Then we iterate over it in order to skip the same product.
                e.g. Bought 'apple, egg' (while buying 'apple', recomd 'egg' only).
                
                The nested loops themselves work like this
                    (1,3,4) => [(1,1), (1,3), (1,4), (3,1), (3,3) ...]
                    
                The combinations itself could be done by
                    `itertools.product(THE_LIST, repeat=HOW_MANY_AS_ONE)`
            
            For the `zincrby()` part, it works like this
                product:01:purchased_with ANY_PROD_ID_BUT_01 SCORE_FOR_2nd_PARAM
                
                The `product_id` is the one you bought.
                THe `with_id`    is the one you bought with. (except product_id)
                
                You use the `product_id` as key,
                    for the things you bought with, they're RANKed (with scores).
                    
            Just to be clear, it IS like a 'product'.
                Combinations as a way, ranking along the way.
                
                Suppose you bought {apple, juice, orange}, it'll be like
                    Apple   =>  juice:  1,   orange: 1
                    Juice   =>  apple:  1,   orange: 1
                    Orange  =>  apple:  1,   juice:  1
            
            ------------------
            
            In short, this method stores
                - product_u_bought
                - product_u_bought_with and scores :D
        """
        
        product_ids = [p.id for p in products]
        
        for product_id in product_ids:
            for with_id in product_ids:
                
                if product_id != with_id:
                    rdb.zincrby(self.get_product_key(product_id),
                                with_id,
                                amount=1)
    
    def suggest_products_for(self, products, max_results=6):
        """
            Just a reminder,
                these methods are tightly connected.
                
            For the parameters,
                products        products we bought
                max_results     how many recommendations being displayed
                
            The `if .. else` represents two scenarios.
        """
        
        #       Product in cart?
        # or    Product we have?
        product_ids = [p.id for p in products]
        
        if len(products) == 1:
            suggestions = rdb.zrange(self.get_product_key(product_ids[0]),
                                     0, -1,
                                     desc=True)[:max_results]
        else:
            # e.g. 'tmp_123'
            flat_ids = ''.join([str(prod_id) for prod_id in product_ids])
            tmp_key = 'tmp_{}'.format(flat_ids)
            
            # e.g. 'product:1:purchased_with'
            keys = [self.get_product_key(prod_id) for prod_id in product_ids]
            
            # Create a replica for `keys` (sort of)
            rdb.zunionstore(tmp_key, keys)
            
            # ** Remove the products that is already "in the cart"
            rdb.zrem(tmp_key, *product_ids)
            
            # Just like 'one product', it's just
            #   the process of 'del-prod-currently-buying' is a bit complicated
            suggestions = rdb.zrange(tmp_key,
                                     0, -1,
                                     desc=True)[:max_results]
            
            # We don't need it anymore (huh)
            rdb.delete(tmp_key)
        
        # This step might caused by 'Redis-return-string-type'
        suggested_products_ids = [int(id) for id in suggestions]
        
        # Get those products, like `<Product: Cookie>`
        suggested_products = list(
                Product.objects.filter(
                        id__in=suggested_products_ids
                )
        )
        
        # Sort by `suggested_products_ids`.
        #   The reason is that the 'xx_ids' have been 'ordered'.
        #   By the work of `products_bought` (=> most recommended).
        suggested_products.sort(
                key=lambda x: suggested_products_ids.index(x.id)
        )
        
        return suggested_products
    
    def clear_purchases(self):
        """
            It clears all the keys in Redis,
                which is being used for recommendation purposes.
        """
        
        for id in Product.objects.values_list('id', flat=True):
            rdb.delete(self.get_product_key(id))