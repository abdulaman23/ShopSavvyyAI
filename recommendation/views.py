from django.shortcuts import render
import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    user_input = request.data.get('query')

    if not user_input:
        return Response({'error': 'Query required'}, status=400)

    headers = {
        "Authorization": f"Bearer {settings.HF_API_TOKEN}"
    }

    payload = {
        "inputs": f"Recommend products based on: {user_input}"
    }

    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return Response({"error": "GenAI response failed"}, status=500)

    genai_output = response.json()[0]['generated_text']
    
    # Dummy logic to simulate filtering (replace with real logic)
    # Ideally you'd extract category/price/brand etc. using NLP
    from catalog.models import Product
    products = Product.objects.filter(title__icontains="laptop")[:5]

    return Response({
        "user_query": user_input,
        "ai_suggestion": genai_output,
        "products": [{
            "id": p.id,
            "title": p.title,
            "price": p.price
        } for p in products]
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chatbot_reply(request):
    user_message = request.data.get('message')

    if not user_message:
        return Response({'error': 'Message required'}, status=400)

    headers = {
        "Authorization": f"Bearer {settings.HF_API_TOKEN}"
    }

    prompt = f"Customer Support Chatbot:\nUser: {user_message}\nBot:"

    payload = {
        "inputs": prompt
    }

    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        return Response({"error": "GenAI response failed"}, status=500)

    reply = response.json()[0]['generated_text'].split("Bot:")[-1].strip()

    return Response({
        "user_message": user_message,
        "chatbot_reply": reply
    })
