```markdown
# Kapru — Kapruka AI Shopping Assistant (Frontend)

A modern, immersive React + Three.js chat interface for the Kapruka Agent Challenge.

## ✨ Features

- 🌍 Rotating 3D globe background with Three.js
- 💬 Full-screen conversational chat UI
- 🛍️ Product cards with images and prices
- ⭐ Animated star field background
- 💜 Beautiful purple gradient design
- 📱 Mobile responsive
- ⚡ Fast and smooth animations
- 🎁 Smart shopping suggestions

## 🛠️ Tech Stack

- React 18 — UI framework
- TypeScript — Type safety
- Vite — Build tool
- Tailwind CSS — Styling
- Three.js — 3D graphics
- @react-three/fiber — React renderer for Three.js
- @react-three/drei — Three.js helpers

```

## 📁 Project Structure


    frontend/
    ├── src/
    │   ├── components/
    │   │   ├── Globe.tsx
    │   │   ├── Header.tsx
    │   │   ├── ChatWindow.tsx
    │   │   ├── MessageBubble.tsx
    │   │   ├── ProductCard.tsx
    │   │   └── TypingIndicator.tsx
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── index.css
    ├── vite.config.ts
    ├── tsconfig.json
    └── package.json



## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- npm

### Installation

```bash
npm install
```

### Development

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

### Production Build

```bash
npm run build
```

## ⚙️ Environment Variables

Create `.env` in frontend folder:

```
VITE_API_URL=https://your-backend.onrender.com
```

Leave empty for local development.

## 🚢 Deployment — Vercel

1. Go to [vercel.com](https://vercel.com)
2. Connect your GitHub repo
3. Set root directory → `frontend`
4. Add env variable `VITE_API_URL`
5. Click Deploy ✅

Auto-deploys on every push to master.

## 🔗 Backend

See [backend/README.md](../backend/README.md)
Backend runs on Render.com

## 🏆 Built For

**Kapruka Agent Challenge 2026**
- Challenge: [kapruka.com](https://kapruka.com)
- MCP docs: [mcp.kapruka.com](https://mcp.kapruka.com)

## 👤 Author

**Namal Dilmith Ruwanpathirana**
- GitHub: [@namal1230](https://github.com/namal1230)

---
© 2026 Kapruka Agent Challenge
