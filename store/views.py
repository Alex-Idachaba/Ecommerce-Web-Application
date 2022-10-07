from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Item, OrderItem, Order, BillingAddress, PostView
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm, ReviewForm
from django.db.models import Q

def about(request):
    context = {

    }
    return render(request, 'about.html', context)

def search(request):
    queryset = Item.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_result.html', context)

class CheckoutView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        #form
        form = CheckoutForm()
        context = {
            'form':form
        }
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid:
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # TODO: add functionalities to these fields
                # same_shipping_address = form.cleaned_data.ge(
                #     'same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                # TODO : add redirect to the selected payment option
                return redirect("store:checkout")
            messages.warning(self.request, "Failed checkout")
            return redirect("store:checkout")
  
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect('store:order_summary')

                
class ItemListView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'store.html'
    context_object_name = 'item_list'

def post_detail(request, slug):
    item = get_object_or_404(Item, slug=slug)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, item=item)

    form = ReviewForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.item = item
            form.save()
            return redirect(reverse("store:product", kwargs={
                'slug': slug
            }))
    context = {
        'item': item,
        'form': form,
    }
    return render(request, 'product.html', context)

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
                }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order.")
            return redirect('/')

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("store:order_summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("store:order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, order_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("store:order_summary")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered = False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("store:order_summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("store:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("store:product", slug=slug)
  
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, 
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered = False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("store:order_summary")
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("store:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("store:product", slug=slug)
