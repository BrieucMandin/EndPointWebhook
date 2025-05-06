import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from data.handlers import process_webhook_payload


@csrf_exempt
def webhook_receiver(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            process_webhook_payload(payload)
            return JsonResponse({'status': 'ok'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)
