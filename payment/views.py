from django.shortcuts import render
# funcion para pago confirmado
def payment_success(request):

	return render(request, "payment/payment_success.html", {})
