from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def process_dispute(request):
    payment_status = request.GET.get('payment_status', None)
    account_status = request.GET.get('account_status', None)
    creditor_remark = request.GET.get('creditor_remark', None)

    try:
        payment_status = int(payment_status)
    except (ValueError, TypeError):
        return JsonResponse({
            "message": "Invalid payment status value.",
            "data": {}
        }, status=400)

    # Logic to generate the dispute letter
    if payment_status >= 30 and account_status in ['paid', 'open']:
        dispute_letter_generated = True
        message = "Dispute letter generated successfully."
        # Placeholder logic for letter creation (add actual file generation here)
    else:
        dispute_letter_generated = False
        message = "Conditions not met for dispute letter."

    # Response data
    response_data = {
        "message": message,
        "data": {
            "payment_status": payment_status,
            "account_status": account_status,
            "creditor_remark": creditor_remark,
            "dispute_letter_generated": dispute_letter_generated
        }
    }

    return JsonResponse(response_data)
