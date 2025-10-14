# Vanna Next.js UI

Modern Next.js web application for Vanna's myDbAssistant - natural language database queries with AI-powered SQL generation.

## ✅ Latest Updates

**v0.2.0 - API Integration Complete**
- ✅ Fixed "The rest of the API is not ported yet" error
- ✅ Added `/api/v0/ask` endpoint for complete Q&A workflow
- ✅ Fixed CORS issues with Next.js proxy
- ✅ Settings page fully functional
- 📚 See [API-INTEGRATION.md](./API-INTEGRATION.md) for details
- 🔧 See [CORS-FIX.md](./CORS-FIX.md) for CORS troubleshooting

## Prerequisites

- **Node.js 18+** ([Download](https://nodejs.org/))
- **Flask backend running** on port 8084 (see `src/myDbAssistant/`)
- **Copilot Socket Core** extension active in VS Code
- **Database** (Oracle/PostgreSQL/MySQL/SQL Server) accessible

## Quick Start

### Option 1: Auto-start Script (Recommended)

```bash
cd ui-nextjs
chmod +x start-dev.sh
./start-dev.sh
```

This script will:
- Stop any existing Flask/Next.js processes
- Start Flask backend on port 8084
- Start Next.js frontend on port 3000
- Verify both services are running

### Option 2: Manual Start

**Terminal 1 - Flask Backend:**
```bash
cd src/myDbAssistant
python3 quick_start_flask_ui.py
```

Wait for:
```
✅ CORS enabled for Next.js frontend (localhost:3000)
✅ Configuration UI enabled at /settings
 * Running on http://0.0.0.0:8084
```

**Terminal 2 - Next.js Frontend:**
```bash
cd ui-nextjs
npm install  # First time only
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Configuration

### Environment Variables

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_FLASK_URL=http://localhost:8084
```

**Note**: In development, Next.js uses a proxy to Flask (no CORS issues). The URL is mainly for production builds.

## Available Scripts

- `npm run dev` - Start development server (port 3000)
- `npm run build` - Create production build
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier
- `npm run type-check` - Run TypeScript compiler check

## Project Structure

```
ui-nextjs/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page (ask questions)
│   │   └── settings/           # Settings page
│   ├── components/             # React components
│   │   ├── ui/                 # Base UI components (Shadcn)
│   │   ├── QuestionInput.tsx
│   │   ├── ResultsDisplay.tsx
│   │   ├── ChartRenderer.tsx
│   │   └── ...
│   ├── lib/                    # Utilities
│   │   ├── api-client.ts       # Flask API client
│   │   ├── types.ts            # TypeScript types
│   │   └── utils.ts            # Helper functions
│   └── hooks/                  # Custom React hooks
├── public/                     # Static assets
└── package.json
```

## Features

- 🤖 **Natural Language Queries** - Ask questions in plain English
- 📊 **Interactive Charts** - Plotly visualizations
- ⚙️ **Settings Management** - Configure LLM, database, and training
- 🎨 **Dark Mode** - Manual theme toggle
- 📱 **Responsive Design** - Mobile-friendly interface
- 🔒 **Type-Safe** - Full TypeScript support

## Configuration

All configurations are managed through the Flask backend API. Use the Settings page to:

- Configure LLM (Copilot Socket Core) settings
- Set up database connections
- Adjust ChromaDB retrieval parameters
- Manage training data

## Troubleshooting

### Flask backend not running
```bash
# Check Flask is running on port 8084
curl http://localhost:8084/api/v0/get_config
```

### CORS issues
The Next.js dev server proxies API requests to avoid CORS issues. Make sure `NEXT_PUBLIC_FLASK_URL` is set correctly.

### Chart rendering issues
Plotly.js requires specific webpack configuration. This is already configured in `next.config.js`.

## Development

### Adding New Components

```bash
# Use Shadcn CLI to add components
npx shadcn-ui@latest add button
```

### API Client

All Flask API calls are centralized in `src/lib/api-client.ts`. Add new endpoints there.

### Type Definitions

TypeScript interfaces are in `src/lib/types.ts` based on Flask API contracts.

## Production Deployment

### Docker

```bash
docker build -t vanna-ui .
docker run -p 3000:3000 -e NEXT_PUBLIC_FLASK_URL=http://flask:8084 vanna-ui
```

### Vercel

```bash
npm run build
# Deploy to Vercel
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Vanna Documentation](https://vanna.ai/docs)
- [Flask Backend](../src/myDbAssistant/README.md)

## License

MIT License - see root [LICENSE](../LICENSE) file.
