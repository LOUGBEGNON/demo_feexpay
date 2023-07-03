import json
import requests
import time

from django.http import JsonResponse
from django.shortcuts import render
from payment.forms import (
    InitPaymentForm,
)

SHOP_ID = '64636955d2ed60e9eac0b9'
API_TOKEN = "fp_9jqqsIq8chG71drXDklEo6kHB6pjEkE0PYZuESPW49hoVBUyE87pSGH0AEsgkk"


def make_request(amount, phone_number, reseau):
    url = 'https://api.feexpay.me/api/transactions/public/requesttopay/mtn'
    if reseau != "" and reseau == "MOOV":
        url = 'https://api.feexpay.me/api/transactions/public/requesttopay/moov'
    headers = {
        "Authorization": f'Bearer {API_TOKEN}',
    }
    data = {
        'shop': SHOP_ID,
        'amount': amount,
        'phoneNumber': phone_number,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200 or response.status_code == 202:
        # Requête réussie
        response_data = response.json()
        reference = response_data.get('reference')  # Récupérer la référence depuis les données JSON

        if reference:
            print("Référence récupérée :", reference)
            return response_data
        else:
            print("Référence non trouvée dans la réponse JSON")
    else:
        # La requête a échoué
        print("Erreur de requête:", response.status_code)


def get_status(reference):
    url = f'https://api.feexpay.me/api/transactions/public/single/status/{reference}'
    headers = {
        "Authorization": f'Bearer {API_TOKEN}',
    }
    try:
        r = requests.get(
            url=url,
            headers=headers
        )
        data = r.json()
        print(data)
        return data
    except Exception as e:
        print(e)
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


# def delayed_request(reference):
#     time.sleep(3)
#     return get_status(reference)


def display_payment_form(request):
    if request.method == 'POST':
        form = InitPaymentForm(request.POST)
        # if form.is_valid():
        #     # Faire quelque chose avec les données du formulaire
        #     phone_number = form.cleaned_data['phone_number']
        #     print(phone_number)
        #     # ...
    else:
        form = InitPaymentForm()

    context = {
        'form': form
    }

    return render(request, 'payment/payment.html', context)


def init_payment(request):
    data = json.loads(request.body)
    phone_number = int(data["phone_number"])
    reseau = data["reseau"]

    if phone_number and reseau != '':
        response_init = make_request(10, phone_number, reseau)
        print(response_init)
        return JsonResponse(response_init, status=200, safe=False)
    # else:
    # return render(request, 'payment/payment.html', context)

def init_payment_card(request):
    data = json.loads(request.body)
    amount = 100
    phone = int(data["phone"])
    reseau = data["reseau"]
    first_name = data['first_name']
    last_name = data['last_name']
    address1 = data['address']
    country = data['country']
    email = data['email']

    if phone and reseau != '' and first_name != '' and last_name != '' and address1 != '' and country != '' and email != '':
        # response_init = make_request(10, phone_number, reseau)
        # print(response_init)
        url = 'https://api.feexpay.me/api/transactions/public/initcard'
        headers = {
            "Authorization": f'Bearer {API_TOKEN}',
        }
        data = {
            'shop': SHOP_ID,
            'amount': amount,
            'phone': phone,
            'last_name': last_name,
            'first_name': first_name,
            'address1': address1,
            'country': country,
            'reseau': reseau,
             # 'currency': 'USD'
        }

        response = requests.post(url, headers=headers, json=data)
        response = response.json()
        return JsonResponse(response, status=200, safe=False)


def get_transaction_status(request):
    reference = json.load(request)["reference"]
    response = get_status(reference)
    return JsonResponse(response, status=200, safe=False)
