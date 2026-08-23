import requests
from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agent import get_agent_response

app = FastAPI(title="SahulatAI Web Application")

# Green API Configuration
GREEN_API_ID = "710722717030"
GREEN_API_TOKEN = "d1f80950ad9f44b4b6b9ef8d0e253c5df92e56b0ccd4428688"  # <-- Yahan apna Green API Token paste karein

# Static files and templates configuration
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryRequest(BaseModel):
    session_id: str
    query: str

@app.get("/", response_class=HTMLResponse)
def serve_chat_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="chat.html"
    )

@app.post("/ask")
def ask_endpoint(payload: QueryRequest):
    response = get_agent_response(payload.session_id, payload.query)
    return {"session_id": payload.session_id, "query": payload.query, "response": response}

# SignalWire / cXML Compatible Inbound Messaging Webhook
@app.post("/signalwire-webhook")
async def signalwire_webhook(From: str = Form(...), Body: str = Form(...)):
    bot_reply = get_agent_response(session_id=From, user_query=Body)
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{bot_reply}</Message>
</Response>"""
    return Response(content=xml_response, media_type="application/xml")

# Green API (WhatsApp) Webhook
@app.post("/whatsapp-webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    
    # Inbound WhatsApp message process karein
    if data.get("typeWebhook") == "incomingMessageReceived":
        sender_id = data["senderData"]["chatId"]
        
        # Message text extract karein
        message_data = data.get("messageData", {})
        user_msg = message_data.get("textMessageData", {}).get("textMessage", "")
        
        if user_msg:
            # RAG pipeline se answer retrieve karein
            bot_reply = get_agent_response(session_id=sender_id, user_query=user_msg)
            
            # WhatsApp par reply send karein
            send_url = f"https://7107.api.greenapi.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"
            payload = {
                "chatId": sender_id,
                "message": bot_reply
            }
            try:
                requests.post(send_url, json=payload, timeout=10)
            except Exception as e:
                print(f"Error sending WhatsApp message: {e}")
            
    return {"status": "ok"}



# import requests
# from fastapi import FastAPI, Request, Form, Response
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from agent import get_agent_response

# app = FastAPI(title="SahulatAI Web Application")

# # Green API Configuration
# GREEN_API_ID = "710722717030"
# GREEN_API_TOKEN = "YOUR_ACTUAL_API_TOKEN_HERE"  # <-- Yahan apna Green API Token paste karein

# # Static files and templates configuration
# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# class QueryRequest(BaseModel):
#     session_id: str
#     query: str

# @app.get("/", response_class=HTMLResponse)
# def serve_chat_page(request: Request):
#     return templates.TemplateResponse(
#         request=request, 
#         name="chat.html"
#     )

# @app.post("/ask")
# def ask_endpoint(payload: QueryRequest):
#     response = get_agent_response(payload.session_id, payload.query)
#     return {"session_id": payload.session_id, "query": payload.query, "response": response}

# # SignalWire / cXML Compatible Inbound Messaging Webhook
# @app.post("/signalwire-webhook")
# async def signalwire_webhook(From: str = Form(...), Body: str = Form(...)):
#     bot_reply = get_agent_response(session_id=From, user_query=Body)
#     xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Message>{bot_reply}</Message>
# </Response>"""
#     return Response(content=xml_response, media_type="application/xml")

# # Green API (WhatsApp) Webhook
# @app.post("/whatsapp-webhook")
# async def whatsapp_webhook(request: Request):
#     data = await request.json()
    
#     # Inbound WhatsApp message process karein
#     if data.get("typeWebhook") == "incomingMessageReceived":
#         sender_id = data["senderData"]["chatId"]
        
#         # Message text extract karein
#         message_data = data.get("messageData", {})
#         user_msg = message_data.get("textMessageData", {}).get("textMessage", "")
        
#         if user_msg:
#             # RAG pipeline se answer retrieve karein
#             bot_reply = get_agent_response(session_id=sender_id, user_query=user_msg)
            
#             # WhatsApp par reply send karein
#             send_url = f"https://7107.api.greenapi.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"
#             payload = {
#                 "chatId": sender_id,
#                 "message": bot_reply
#             }
#             try:
#                 requests.post(send_url, json=payload, timeout=10)
#             except Exception as e:
#                 print(f"Error sending WhatsApp message: {e}")
            
#     return {"status": "ok"}







# from fastapi import FastAPI, Request, Form, Response
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from agent import get_agent_response

# app = FastAPI(title="SahulatAI Web Application")

# # Static files and templates configuration
# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# class QueryRequest(BaseModel):
#     session_id: str
#     query: str

# @app.get("/", response_class=HTMLResponse)
# def serve_chat_page(request: Request):
#     return templates.TemplateResponse(
#         request=request, 
#         name="chat.html"
#     )

# @app.post("/ask")
# def ask_endpoint(payload: QueryRequest):
#     response = get_agent_response(payload.session_id, payload.query)
#     return {"session_id": payload.session_id, "query": payload.query, "response": response}

# # SignalWire / Twilio Compatible Inbound Messaging Webhook
# @app.post("/signalwire-webhook")
# async def signalwire_webhook(From: str = Form(...), Body: str = Form(...)):
#     # Query ko RAG agent pipeline se process karein
#     bot_reply = get_agent_response(session_id=From, user_query=Body)
    
#     # SignalWire / cXML XML response format
#     xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
# <Response>
#     <Message>{bot_reply}</Message>
# </Response>"""
    
#     return Response(content=xml_response, media_type="application/xml")






# # from fastapi import FastAPI, Request
# # from fastapi.responses import HTMLResponse
# # from fastapi.templating import Jinja2Templates
# # from pydantic import BaseModel
# # from agent import get_agent_response
# # from fastapi.staticfiles import StaticFiles

# # app = FastAPI(title="SahulatAI Web Application")
# # templates = Jinja2Templates(directory="templates")
# # app.mount("/static", StaticFiles(directory="static"), name="static")

# # class QueryRequest(BaseModel):
# #     session_id: str
# #     query: str

# # @app.get("/", response_class=HTMLResponse)
# # def serve_chat_page(request: Request):
# #     return templates.TemplateResponse(
# #         request=request, 
# #         name="chat.html"
# #     )

# # @app.post("/ask")
# # def ask_endpoint(payload: QueryRequest):
# #     response = get_agent_response(payload.session_id, payload.query)
# #     return {"session_id": payload.session_id, "query": payload.query, "response": response}





