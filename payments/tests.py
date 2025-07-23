from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from cart.cart import Cart
from shop.models import Product, Category
from orders.models import Order
from users.models import UserProfile

class PaymentsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        # Check if a profile already exists, otherwise create one
        try:
            self.user.userprofile = UserProfile.objects.get(user=self.user)
        except UserProfile.DoesNotExist:
            self.user.userprofile = UserProfile.objects.create(user=self.user)

        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=10.00
        )
        # Add product to cart using a request object
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1, 'update': False})


    def test_checkout_redirects_to_payeer(self):
        # Add something to the cart
        self.client.post(reverse('cart:cart_add', args=[self.product.id]), {'quantity': 1, 'update': False})
        response = self.client.get(reverse('payments:checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('https://payeer.com/merchant/'))

    def test_payment_success(self):
        order = Order.objects.create(user=self.user, paid=False)
        response = self.client.get(reverse('payments:payment_success') + f'?m_orderid={order.id}')
        order.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(order.paid)
        self.assertContains(response, f'Your order #{order.id} has been placed successfully!')

    def test_payment_cancelled(self):
        response = self.client.get(reverse('payments:payment_cancelled'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Payment was cancelled.')
