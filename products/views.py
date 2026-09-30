from decimal import Decimal

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib import messages

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from django.contrib.auth.models import User

from django.db import transaction

from .models import (
    Category,
    Product,
    Order,
    OrderItem
)

from .forms import CheckoutForm


# =====================================================
# HELPERS
# =====================================================

def get_cart_count(request):
    cart = request.session.get("cart", {})
    return sum(int(v) for v in cart.values())


# =====================================================
# HOME
# =====================================================

def home(request):
    categories = Category.objects.all()
    products = Product.objects.select_related("category").all().order_by("-created_at")

    return render(
        request,
        "home.html",
        {
            "categories": categories,
            "products": products,
        }
    )


# =====================================================
# ADD TO CART
# =====================================================

def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})

    product_key = str(product_id)

    current_quantity = int(cart.get(product_key, 0))

    if current_quantity >= product.stock:
        messages.error(
            request,
            f"Sorry, only {product.stock} items of '{product.name}' are available."
        )
    else:
        cart[product_key] = current_quantity + 1
        request.session["cart"] = cart
        messages.success(
            request,
            f"'{product.name}' added to cart."
        )

    # Redirect back to where the user came from
    referer = request.META.get("HTTP_REFERER", "")
    if referer:
        return redirect(referer)
    return redirect("home")


# =====================================================
# BUY NOW
# =====================================================

def buy_now(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(
            request,
            f"'{product.name}' is currently out of stock."
        )
        referer = request.META.get("HTTP_REFERER", "")
        if referer:
            return redirect(referer)
        return redirect("home")

    # Replace cart with only this product
    request.session["cart"] = {str(product.id): 1}
    request.session.modified = True

    return redirect("checkout")


# =====================================================
# CART
# =====================================================

def cart_view(request):

    cart = request.session.get("cart", {})

    cart_items = []
    subtotal = Decimal("0.00")

    for product_id, quantity in cart.items():
        try:
            product = get_object_or_404(Product, id=product_id)
            quantity = int(quantity)
            item_total = product.price * quantity
            subtotal += item_total
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "total": item_total,
            })
        except Exception:
            continue

    delivery_fee = (
        Decimal("0.00")
        if subtotal >= Decimal("999")
        else Decimal("49.00")
    )

    total = subtotal + delivery_fee

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "total": total,
        }
    )


# =====================================================
# UPDATE CART
# =====================================================

def update_cart(request, product_id):

    if request.method != "POST":
        return redirect("cart")

    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get("quantity", 1))

    cart = request.session.get("cart", {})
    product_key = str(product_id)

    if quantity <= 0:
        cart.pop(product_key, None)
    elif quantity <= product.stock:
        cart[product_key] = quantity
    else:
        cart[product_key] = product.stock
        messages.warning(
            request,
            f"Only {product.stock} items of '{product.name}' available."
        )

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# =====================================================
# REMOVE FROM CART
# =====================================================

def remove_from_cart(request, product_id):

    cart = request.session.get("cart", {})
    cart.pop(str(product_id), None)
    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


# =====================================================
# CHECKOUT
# =====================================================

def checkout(request):

    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    cart_items = []
    subtotal = Decimal("0.00")

    for product_id, quantity in cart.items():
        try:
            product = get_object_or_404(Product, id=product_id)
            quantity = int(quantity)
            item_total = product.price * quantity
            subtotal += item_total
            cart_items.append({
                "product": product,
                "quantity": quantity,
                "total": item_total,
            })
        except Exception:
            continue

    delivery_fee = (
        Decimal("0.00")
        if subtotal >= Decimal("999")
        else Decimal("49.00")
    )

    discount = Decimal("0.00")
    coupon_code = ""

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            coupon_code = (
                form.cleaned_data["coupon"].strip().upper()
            )

            # Apply coupon
            if coupon_code == "GLOW10":
                discount = subtotal * Decimal("0.10")
            elif coupon_code == "BEAUTY200":
                discount = min(Decimal("200.00"), subtotal)

            total = subtotal + delivery_fee - discount

            # =========================================
            # CREATE ORDER
            # =========================================

            try:
                with transaction.atomic():

                    order = Order.objects.create(
                        user=(
                            request.user
                            if request.user.is_authenticated
                            else None
                        ),
                        full_name=form.cleaned_data["full_name"],
                        email=form.cleaned_data["email"],
                        phone=form.cleaned_data["phone"],
                        address=form.cleaned_data["address"],
                        city=form.cleaned_data["city"],
                        state=form.cleaned_data["state"],
                        pincode=form.cleaned_data["pincode"],
                        payment_method=form.cleaned_data["payment_method"],
                        subtotal=subtotal,
                        discount=discount,
                        delivery_fee=delivery_fee,
                        total=total,
                        coupon_code=coupon_code,
                    )

                    for item in cart_items:
                        product = item["product"]
                        qty = item["quantity"]

                        if qty > product.stock:
                            raise ValueError(
                                f"Not enough stock for '{product.name}'"
                            )

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            product_name=product.name,
                            price=product.price,
                            quantity=qty,
                        )

                        product.stock -= qty
                        product.save(update_fields=["stock"])

                # Clear cart
                request.session["cart"] = {}
                request.session.modified = True

                return redirect("order_success", order_id=order.id)

            except ValueError as e:
                messages.error(request, str(e))

    else:
        form = CheckoutForm()

    return render(
        request,
        "checkout.html",
        {
            "form": form,
            "cart_items": cart_items,
            "subtotal": subtotal,
            "delivery_fee": delivery_fee,
            "discount": discount,
            "total": subtotal + delivery_fee - discount,
        }
    )


# =====================================================
# ORDER SUCCESS
# =====================================================

def order_success(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    return render(
        request,
        "order_success.html",
        {"order": order}
    )


# =====================================================
# LOGIN
# =====================================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


# =====================================================
# REGISTER
# =====================================================

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email", "")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("home")

    return render(request, "register.html")


# =====================================================
# LOGOUT
# =====================================================

def logout_view(request):
    logout(request)
    return redirect("home")