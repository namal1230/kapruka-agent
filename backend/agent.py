import google.generativeai as genai
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MCP_URL = "https://mcp.kapruka.com/mcp"

TOOLS = [
    {
        "name": "kapruka_search_products",
        "description": "Search Kapruka products by keyword, category, price range.",
        "parameters": {
            "type": "object",
            "properties": {
                "q": {
                    "type": "string",
                    "description": "Search keyword"
                },
                "category": {
                    "type": "string",
                    "description": "Product category"
                },
                "min_price": {
                    "type": "number",
                    "description": "Minimum price"
                },
                "max_price": {
                    "type": "number",
                    "description": "Maximum price"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results"
                },
                "currency": {
                    "type": "string",
                    "description": "Currency code like LKR"
                }
            },
            "required": ["q"]
        }
    },
    {
        "name": "kapruka_get_product",
        "description": "Get full details of a product by ID",
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "Product ID"
                },
                "currency": {
                    "type": "string",
                    "description": "Currency code like LKR"
                }
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "kapruka_list_categories",
        "description": "List all product categories on Kapruka",
        "parameters": {
            "type": "object",
            "properties": {
                "depth": {
                    "type": "integer",
                    "description": "Category tree depth"
                }
            }
        }
    },
    {
        "name": "kapruka_list_delivery_cities",
        "description": "Search delivery cities in Sri Lanka",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "City name to search"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results"
                }
            }
        }
    },
    {
        "name": "kapruka_check_delivery",
        "description": "Check if delivery is possible to a city on a date",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Delivery city name"
                },
                "delivery_date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format"
                },
                "product_id": {
                    "type": "string",
                    "description": "Product ID"
                }
            },
            "required": ["city", "delivery_date", "product_id"]
        }
    },
    {
        "name": "kapruka_create_order",
        "description": "Create guest checkout order and return payment link",
        "parameters": {
            "type": "object",
            "properties": {
                "cart": {
                    "type": "array",
                    "description": "List of products",
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_id": {
                                "type": "string"
                            },
                            "quantity": {
                                "type": "integer"
                            }
                        }
                    }
                },
                "recipient": {
                    "type": "string",
                    "description": "Recipient details as JSON string with name, phone, address, city"
                },
                "delivery": {
                    "type": "string",
                    "description": "Delivery details as JSON string with date"
                },
                "sender": {
                    "type": "string",
                    "description": "Sender details as JSON string with name, phone, email"
                },
                "gift_message": {
                    "type": "string",
                    "description": "Optional gift message"
                },
                "currency": {
                    "type": "string",
                    "description": "Currency code like LKR"
                }
            },
            "required": ["cart", "recipient", "delivery"]
        }
    },
    {
        "name": "kapruka_track_order",
        "description": "Track existing Kapruka order by order number",
        "parameters": {
            "type": "object",
            "properties": {
                "order_number": {
                    "type": "string",
                    "description": "Order number from confirmation"
                }
            },
            "required": ["order_number"]
        }
    }
]

SYSTEM_PROMPT = """You are Kapru 🛍️, a warm and helpful AI shopping assistant 
for Kapruka.com — Sri Lanka's largest online shop.

## Your Personality
- Friendly, warm and conversational
- Use emojis naturally but not excessively
- Be concise but helpful
- Support both English and Sinhala languages
- Feel like chatting with a knowledgeable friend

## Your Capabilities
- Search products by keyword or category
- Show product details with prices in LKR
- Check delivery availability to any Sri Lankan city
- Help create orders with gift messages
- Track existing orders

## Shopping Flow
1. Understand what the customer wants
2. Search and show relevant products
3. Help them pick the right one
4. Collect delivery details
5. Check delivery availability
6. Create order and provide payment link

## When Showing Products
- Show name, price in LKR, key details
- Mention if in stock
- Ask if they want to order or see more options
- Show max 4-5 products at a time

## When Creating Orders
Collect in this order:
1. Confirm product and quantity
2. Ask if it's a gift (offer gift message)
3. Get recipient name, phone, address, city
4. Ask preferred delivery date
5. Get sender name, phone, email
6. Create order and share payment link

## Important Rules
- Always be helpful and guide to checkout
- If product not found, suggest alternatives
- For cakes/flowers mention delivery date constraints
- Always confirm order details before creating
- Never make up product details or prices

## Language
- Respond in the same language the user writes in
- Support Sinhala: ආයුබෝවන් (Ayubowan)
- Support Tanglish (Tamil + English mix)"""


async def call_mcp_tool(tool_name: str, tool_input: dict):
    """Call a Kapruka MCP tool"""
    try:
        async with httpx.AsyncClient(timeout=30) as http_client:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": tool_input
                }
            }
            response = await http_client.post(
                MCP_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            result = response.json()
            print(f"MCP Result for {tool_name}: {result}")
            return result.get("result", {})
    except Exception as e:
        print(f"MCP Error: {e}")
        return {"error": str(e)}


async def chat(messages: list) -> str:
    """Chat with Gemini + Kapruka MCP tools"""
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT,
            tools=[{"function_declarations": TOOLS}]
        )

        gemini_history = []
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({
                "role": role,
                "parts": [msg["content"]]
            })

        chat_session = model.start_chat(
            history=gemini_history
        )

        last_message = messages[-1]["content"]
        response = chat_session.send_message(last_message)

        max_iterations = 5
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            tool_calls = []

            for part in response.parts:
                if hasattr(part, "function_call") and part.function_call.name:
                    tool_calls.append(part.function_call)

            if not tool_calls:
                break

            tool_results = []
            for tool_call in tool_calls:
                tool_name = tool_call.name
                tool_input = dict(tool_call.args)

                print(f"🔧 Calling: {tool_name}")
                print(f"📥 Input: {tool_input}")

                result = await call_mcp_tool(
                    tool_name,
                    tool_input
                )

                tool_results.append(
                    genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=tool_name,
                            response={
                                "result": json.dumps(result)
                            }
                        )
                    )
                )

            response = chat_session.send_message(
                tool_results
            )

        final_text = ""
        for part in response.parts:
            if hasattr(part, "text") and part.text:
                final_text += part.text

        return final_text if final_text else \
            "Sorry, I could not process that. Please try again!"

    except Exception as e:
        print(f"❌ Chat Error: {e}")
        return f"Sorry, something went wrong: {str(e)}"