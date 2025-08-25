import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
stripe.api_key = settings.STRIPE_SECRET_KEY

# Fixed conversion rate for demonstration. You should use a real-time API.
# Example: 1 USD = 108 BDT
BDT_TO_USD_RATE = 1 / 108

@csrf_exempt
def create_payment(request):
    """
    Creates a Stripe PaymentIntent after converting the amount from BDT to USD.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount_bdt = data.get('amount_bdt')
            if amount_bdt is None:
                return JsonResponse({'error': 'Amount in BDT is required'}, status=400)

            # Convert BDT to USD
            amount_usd = amount_bdt * BDT_TO_USD_RATE
            
            # Create a PaymentIntent with the converted USD amount and currency
            # Stripe requires amount in cents and as an integer.
            amount_in_cents = int(amount_usd * 100)
            
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,  
                currency='usd',
                payment_method_types=['card'],
            )
            return JsonResponse({
                'clientSecret': intent.client_secret,
                'amount_usd': amount_usd # Return the USD amount to the frontend
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
