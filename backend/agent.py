import anthropic
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

MCP_URL = "https://mcp.kapruka.com/mcp"

TOOLS = [
    {
        "name": "kapruka_search_products",
        "description": "Search Kapruka products by keyword, category, price range. Use this when user asks for any product.",
        "input_schema": {
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
                "in_stock_only": {
                    "type": "boolean",
                    "description": "Only show in stock items"
                },
                "limit": {
                    "type": "integer",
                    "description": "Number of results"
                },
                "currency": {
                    "type": "string",
                    "default": "LKR"
                }
            },
            "required": ["q"]
        }
    },
    {
        "name": "kapruka_get_product",
        "description": "Get full details of a specific product by ID including images, variants, shipping info",
        "input_schema": {
            "type": "object",
            "properties": {
                "product_id": {
                    "type": "string",
                    "description": "Product ID from search results"
                },
                "currency": {
                    "type": "string",
                    "default": "LKR"
                }
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "kapruka_list_categories",
        "description": "List all available product categories on Kapruka",
        "input_schema": {
            "type": "object",
            "properties": {
                "depth": {
                    "type": "integer",
                    "description": "Depth of category tree"
                }
            }
        }
    },
    {
        "name": "kapruka_list_delivery_cities",
        "description": "Search delivery cities available in Sri Lanka",
        "input_schema": {
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
        "description": "Check if delivery is possible to a city on a specific date for a product",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Delivery city name"
                },
                "delivery_date": {
                    "type": "string",
                    "description": "Delivery date in YYYY-MM-DD format"
                },
                "product_id": {
                    "type": "string",
                    "description": "Product ID to check"
                }
            },
            "required": ["city", "delivery_date", "product_id"]
        }
    },
    {
        "name": "kapruka_create_order",
        "description": "Create a guest checkout order and return a click-to-pay link. No Kapruka account needed.",
        "input_schema": {
            "type": "object",
            "properties": {
                "cart": {
                    "type": "array",
                    "description": "List of items with product_id and quantity",
                    "items": {
                        "type": "object",
                        "properties": {
                            "product_id": {"type": "string"},
                            "quantity": {"type": "integer"}
                        }
                    }
                },
                "recipient": {
                    "type": "object",
                    "description": "Recipient details",
                    "properties": {
                        "name": {"type": "string"},
                        "phone": {"type": "string"},
                        "address": {"type": "string"},
                        "city": {"type": "string"}
                    }
                },
                "delivery": {
                    "type": "object",
                    "description": "Delivery details",
                    "properties": {
                        "date": {"type": "string"},
                        "time_slot": {"type": "string"}
                    }
                },
                "sender": {
                    "type": "object",
                    "description": "Sender details",
                    "properties": {
                        "name": {"type": "string"},
                        "phone": {"type": "string"},
                        "email": {"type": "string"}
                    }
                },
                "gift_message": {
                    "type": "string",
                    "description": "Optional gift message"
                },
                "currency": {
                    "type": "string",
                    "default": "LKR"
                }
            },
            "required": ["cart", "recipient", "delivery"]
        }
    },
    {
        "name": "kapruka_track_order",
        "description": "Track an existing Kapruka order status and delivery progress",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_number": {
                    "type": "string",
                    "description": "Order number from confirmation email"
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
    """Main chat function with tool calling"""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages
        )

        while response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    print(f"🔧 Tool: {block.name}")
                    print(f"📥 Input: {block.input}")

                    result = await call_mcp_tool(
                        block.name,
                        block.input
                    )

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })

            messages = messages + [
                {
                    "role": "assistant",
                    "content": response.content
                },
                {
                    "role": "user",
                    "content": tool_results
                }
            ]

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages
            )

        final_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                final_text += block.text

        return final_text

    except Exception as e:
        print(f"Chat Error: {e}")
        return f"Sorry, I encountered an error: {str(e)}"