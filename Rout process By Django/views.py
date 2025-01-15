from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view
from rest_framework.response import Response

def generate_dispute_letter(data):
    """
    Generate a PDF dispute letter.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, f"Payment Status: {data['payment_status']}")
    p.drawString(100, 730, f"Account Status: {data['account_status']}")
    p.drawString(100, 710, f"Creditor Remark: {data['creditor_remark']}")
    p.drawString(100, 690, "This is a generated dispute letter.")
    p.save()
    buffer.seek(0)
    return buffer

@api_view(['GET'])
def process_dispute(request):
    payment_status = request.GET.get('payment_status', None)
    account_status = request.GET.get('account_status', None)
    creditor_remark = request.GET.get('creditor_remark', None)

    try:
        payment_status = int(payment_status)
    except (ValueError, TypeError):
        return Response({
            "message": "Invalid payment status value.",
            "data": {}
        }, status=400)

    # Logic to determine if a dispute letter should be generated
    if payment_status >= 30 and account_status in ['paid', 'open']:
        dispute_letter_generated = True
        message = "Dispute letter generated successfully."
        
        # Generate the PDF file
        pdf_buffer = generate_dispute_letter({
            "payment_status": payment_status,
            "account_status": account_status,
            "creditor_remark": creditor_remark,
        })
        
        # Return the PDF as a response
        return HttpResponse(pdf_buffer, content_type='application/pdf')
    else:
        dispute_letter_generated = False
        message = "Conditions not met for dispute letter."

    # Response for cases where no letter is generated
    response_data = {
        "message": message,
        "data": {
            "payment_status": payment_status,
            "account_status": account_status,
            "creditor_remark": creditor_remark,
            "dispute_letter_generated": dispute_letter_generated
        }
    }

    return Response(response_data, status=200)
