```markdown
# Kapru Backend — Kapruka AI Shopping Agent

AI-powered shopping assistant backend for Kapruka.com built with FastAPI and Google Gemini.

## ✨ Features

- 🤖 Google Gemini AI powered conversations
- 🛍️ Kapruka MCP integration — no API key needed
- 🔍 Real-time product search
- 🚚 Delivery availability checking
- 💳 Guest checkout order creation
- 📦 Order tracking
- 🌐 CORS enabled for frontend connection
- 📖 Auto Swagger documentation

## 🛠️ Tech Stack

- **FastAPI** — Web framework
- **Python 3.10+** — Language
- **Google Gemini 2.0 Flash** — AI model (free)
- **Kapruka MCP** — Shopping tools (free)
- **httpx** — Async HTTP client
- **uvicorn** — ASGI server

## 📁 Project Structure

    backend/
    ├── agent.py          # Gemini AI + MCP tool calling logic
    ├── main.py           # FastAPI app and endpoints
    ├── requirements.txt  # Python dependencies
    ├── .env              # Environment variables (not in git)
    └── .gitignore        # Git ignore rules

```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API key (free at aistudio.google.com)

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create `.env` file in backend folder:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your FREE key at:
👉 `aistudio.google.com` → Get API Key → Create API Key

### Run Development Server

```bash
python main.py
```

Server runs at `http://localhost:8000`

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Send message to AI agent |
| GET | `/health` | Health check |
| GET | `/` | Root info |
| GET | `/docs` | Swagger UI |

### Example Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Show me birthday cakes"
      }
    ]
  }'
```

### Example Response

```json
{
  "response": "Here are some birthday cakes 🎂 from Kapruka..."
}
```

## 🔧 Kapruka MCP Tools

All tools are FREE — no API key needed!

| Tool | Description |
|------|-------------|
| `kapruka_search_products` | Search product catalog |
| `kapruka_get_product` | Get product details by ID |
| `kapruka_list_categories` | Browse all categories |
| `kapruka_list_delivery_cities` | Find delivery cities |
| `kapruka_check_delivery` | Check delivery availability |
| `kapruka_create_order` | Create guest checkout order |
| `kapruka_track_order` | Track order status |

MCP Endpoint: `https://mcp.kapruka.com/mcp`

## 🚢 Deployment — Render.com (Free)


## 🔗 Frontend

React frontend connects to this backend.
See [frontend/README.md](../frontend/README.md)

Frontend deployed on Vercel.com

## 🏆 Built For

**Kapruka Agent Challenge 2026**
- Challenge: [kapruka.com](https://kapruka.com)
- MCP docs: [mcp.kapruka.com](https://mcp.kapruka.com)
- Deadline: 30 June 2026

## 💡 How It Works

```
User Message
     ↓
FastAPI /chat endpoint
     ↓
Gemini 2.0 Flash (understands intent)
     ↓
Calls Kapruka MCP tools
     ↓
Gets real product data
     ↓
Gemini formats response
     ↓
Returns to user
```

## 👤 Author

**Namal Dilmith Ruwanpathirana**
- GitHub: [@namal1230](https://github.com/namal1230)
- Email: ndilmith2002@gmail.com

---
© 2026 Kapruka Agent Challenge
