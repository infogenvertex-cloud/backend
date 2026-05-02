from __future__ import annotations

import json
import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

# ============================================================
# GUPSHUP INTEGRATION (COMMENTED OUT)
# ============================================================
# GUPSHUP_URL = "https://api.gupshup.io/wa/api/v1/msg"
#
# async def send_text_message(phone: str, text: str) -> dict | None:
#     if not settings.GUPSHUP_API_KEY:
#         logger.warning("Gupshup API key not configured.")
#         return None
#     async with httpx.AsyncClient() as client:
#         payload = {
#             "channel": "whatsapp",
#             "source": settings.GUPSHUP_SOURCE_NUMBER,
#             "destination": phone,
#             "message": json.dumps({"type": "text", "text": text}),
#             "src.name": settings.GUPSHUP_APP_NAME,
#         }
#         headers = {"apikey": settings.GUPSHUP_API_KEY}
#         try:
#             response = await client.post(GUPSHUP_URL, data=payload, headers=headers)
#             response.raise_for_status()
#             return response.json()
#         except httpx.HTTPError as e:
#             logger.error(f"Failed to send WhatsApp message to {phone}: {e}")
#             return None
#
# async def send_invoice(phone: str, invoice_url: str, member_name: str) -> dict | None:
#     if not settings.GUPSHUP_API_KEY:
#         logger.warning("Gupshup API key not configured.")
#         return None
#     async with httpx.AsyncClient() as client:
#         payload = {
#             "channel": "whatsapp",
#             "source": settings.GUPSHUP_SOURCE_NUMBER,
#             "destination": phone,
#             "message": json.dumps({
#                 "type": "file",
#                 "url": invoice_url,
#                 "filename": f"invoice_{member_name}.pdf",
#             }),
#             "src.name": settings.GUPSHUP_APP_NAME,
#         }
#         headers = {"apikey": settings.GUPSHUP_API_KEY}
#         try:
#             response = await client.post(GUPSHUP_URL, data=payload, headers=headers)
#             response.raise_for_status()
#             return response.json()
#         except httpx.HTTPError as e:
#             logger.error(f"Failed to send invoice to {phone}: {e}")
#             return None


# ============================================================
# WHATSAPP CLOUD API (META) INTEGRATION
# ============================================================
# Docs: https://developers.facebook.com/docs/whatsapp/cloud-api
#
# Required .env variables:
#   WHATSAPP_TOKEN=your_permanent_access_token
#   WHATSAPP_PHONE_ID=your_phone_number_id
#
# Setup steps:
# 1. Go to https://developers.facebook.com
# 2. Create an app → select "Business" type
# 3. Add "WhatsApp" product
# 4. Get Phone Number ID and Access Token from WhatsApp > API Setup
# 5. Add your .env values
# ============================================================

WHATSAPP_API_URL = "https://graph.facebook.com/v21.0"


async def send_text_message(phone: str, text: str) -> dict | None:
    """Send a text message via WhatsApp Cloud API."""
    if not settings.WHATSAPP_TOKEN or not settings.WHATSAPP_PHONE_ID:
        logger.warning("WhatsApp Cloud API not configured. Skipping message.")
        return None

    url = f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": text},
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"WhatsApp text sent to {phone}")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to send WhatsApp message to {phone}: {e}")
            return None


async def send_invoice(phone: str, invoice_url: str, member_name: str) -> dict | None:
    """Send invoice PDF via WhatsApp Cloud API."""
    if not settings.WHATSAPP_TOKEN or not settings.WHATSAPP_PHONE_ID:
        logger.warning("WhatsApp Cloud API not configured. Skipping invoice.")
        return None

    url = f"{WHATSAPP_API_URL}/{settings.WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "document",
        "document": {
            "link": invoice_url,
            "filename": f"Marvel_Fitness_Invoice_{member_name}.pdf",
            "caption": f"Hi {member_name}, here is your payment invoice from Marvel Fitness. Thank you!",
        },
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logger.info(f"WhatsApp invoice sent to {phone}")
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Failed to send invoice to {phone}: {e}")
            return None
