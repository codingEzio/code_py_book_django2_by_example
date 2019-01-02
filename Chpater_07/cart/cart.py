from decimal import Decimal

from django.conf import settings

from shop.models import Product
from coupons.models import Coupon


class Cart(object):
    """
        The notes I've taken for now
            is not entirely valid for all
            since we haven't used each one of them!
    """
    
    def __init__(self, request):
        """
            We're first trying to get the current session
                Nothing =>  Init a null dict (session['cart'] = all-of-our-stuff)
                Gotcha  =>  Simply assign the val to the 'cart' (inst variable)
                
            The structure inside the dict <might> be
                like this: '{'1': {'apple': 6}, '2': {'orange': 10}}'
        """
        
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = { }
        
        self.cart = cart
        
        self.coupon_id = self.session.get('coupon_id')
    
    def add(self, product, quantity=1, update_quantity=False):
        """
            ---- Lemme trans the code into plain words ----
            
            [not in self.cart]
                I didn't put it in the cart  ->  init the 'quantity' & 'price'
                
            [update_quantity]
                It only'll be added (quantity)
                
                As long as it's not True,
                    since there's no explicit way to change it (indeed).
                    
            [self.save()]
                Change the state of session
                    by calling the subsequent method 'save'.
        """
        
        # N -> 'N' -> cart['N']
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = { 'quantity': 0,
                                      'price'   : str(product.price) }
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
    
    def save(self):
        """
            Simply for changing the state of 'cart' session :D
        """
        
        self.session.modified = True
    
    def remove(self, product):
        """
            Simply del a key in the 'cart' session (with its val of course!)
        """
        
        product_id = str(product.id)
        
        if product_id in self.cart:
            del self.cart[product_id]
            
            self.save()
    
    def __iter__(self):
        """
            [First-two-lines]
                Get the IDs of the products that I've put into the <cart>
                    then get each corresponding products (thus the 'name' XD)
                
            [One-copy-and-two-loops]
                Get a copy of the <cart> (storing our (not null) carts)
                
                'product'
                    Storing the names of the products
                
                item
                    Assigning the internal vals to the key 'product' (maybe?)
        """
        
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            
            yield item
    
    def __len__(self):
        """
            The quantities of all the cart items (don't overthink).
                It's kinda ugly, well... I haven't found the other ways!
        """
        
        return sum(
            item['quantity']
            for item in self.cart.values()
        )
    
    def get_total_price(self):
        """
            Kinda the same mechanics as the func '__len__()'
                Get those values & then calc the <total prices> :D
        """
        
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )
    
    def clear(self):
        """
            Delete all of the content inside the session['cart']
        """
        
        del self.session[settings.CART_SESSION_ID]
        
        self.save()
    
    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        
        return None  # exec if not getting ID
    
    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        
        return Decimal('0')  # no discount if there's no coupon
    
    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()