from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db import transaction
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.views import get_cart

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
@login_required
def cancel_order_view(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if request.method == 'POST':
        if order.status != 'pending':
            messages.error(request, 'Only pending orders can be cancelled.')
        else:
            with transaction.atomic():
                order.status = 'cancelled'
                order.save()

                # Restore stock
                for item in order.items.select_related('product'):
                    item.product.stock = F('stock') + item.quantity
                    item.product.save()

            messages.success(request, f'Order #{order.order_number} has been cancelled.')
    else:
        messages.error(request, 'Invalid request method.')

    return redirect('orders:list')

from django.db.models import F

@login_required
def checkout_view(request):
    cart = get_cart(request)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart:view')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Stock check
                for cart_item in cart.items.select_related('product'):
                    product = cart_item.product
                    if product.stock < cart_item.quantity:
                        messages.error(request, f"Not enough stock for '{product.name}'. Only {product.stock} left.")
                        return redirect('cart:view')
                
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=cart.total_price,
                    billing_name=form.cleaned_data['billing_name'],
                    billing_email=form.cleaned_data['billing_email'],
                    billing_phone=form.cleaned_data['billing_phone'],
                    billing_address=form.cleaned_data['billing_address'],
                    billing_city=form.cleaned_data['billing_city'],
                    billing_state=form.cleaned_data['billing_state'],
                    billing_zipcode=form.cleaned_data['billing_zipcode'],
                    billing_country=form.cleaned_data['billing_country'],
                    shipping_name=form.cleaned_data['shipping_name'],
                    shipping_address=form.cleaned_data['shipping_address'],
                    shipping_city=form.cleaned_data['shipping_city'],
                    shipping_state=form.cleaned_data['shipping_state'],
                    shipping_zipcode=form.cleaned_data['shipping_zipcode'],
                    shipping_country=form.cleaned_data['shipping_country'],
                )
                
                # Create order items and deduct stock safely
                for cart_item in cart.items.select_related('product'):
                    product = cart_item.product
                    
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        product_price=product.price,
                        quantity=cart_item.quantity
                    )
                    
                    # Safely decrement stock
                    product.stock = F('stock') - cart_item.quantity
                    product.save()
                
                # Clear cart
                cart.items.all().delete()
                
                messages.success(request, f'Order {order.order_number} placed successfully!')
                return redirect('orders:detail', pk=order.pk)
    else:
        # Pre-fill form with user data
        initial_data = {
            'billing_name': f"{request.user.first_name} {request.user.last_name}",
            'billing_email': request.user.email,
            'billing_phone': request.user.phone,
            'billing_address': request.user.address,
            'billing_city': request.user.city,
            'billing_state': request.user.state,
            'billing_zipcode': request.user.zipcode,
            'billing_country': request.user.country,
        }
        form = CheckoutForm(initial=initial_data)
    
    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart
    })