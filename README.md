# Hospital Voice Assistant

A real-time AI-powered voice assistant for hospitals built using FastAPI, LiveKit, and React.  
The system allows users to interact via voice to book appointments, check doctor availability, and handle hospital-related queries efficiently.

---

## Features

- Real-time voice interaction  
- AI-based voice agent (voice pipeline)  
- Voice-driven appointment booking  
- Doctor availability and slot management  
- Live communication using LiveKit  
- Full-stack integration (React + FastAPI)  
- High-performance backend with FastAPI  

---

## System Architecture

```
User (Voice)
   ↓
React Frontend (LiveKit Client)
   ↓
LiveKit Server (Voice Stream)
   ↓
Voice Agent (Processing Layer)
   ↓
FastAPI Backend
   ↓
Database (Doctors, Slots, Appointments)
```

---

## Tech Stack

### Frontend
- React (Vite)  
- LiveKit Client SDK  
- Axios  

### Backend
- FastAPI  
- Python  
- LiveKit Server SDK  

### Deployment
- Railway (Backend)  
- Vercel (Frontend)  

---

## Project Structure

### Backend

```
backend/
│
├── agent/        # Voice agent logic (pipeline, session handling)
├── api/          # API routes
├── core/         # App configuration (CORS, settings)
├── crud/         # Database operations
├── data/         # Seed/static data
├── models/       # Database models
├── schemas/      # Pydantic schemas
│
├── database.py   # Database connection
├── main.py       # FastAPI entry point
├── railway.json
└── requirements.txt
```

### Frontend

```
frontend/
│
├── src/
│   ├── api/         # API configuration
│   ├── assets/      # Static files
│   ├── components/  # UI components
│   ├── context/     # Global state
│   ├── pages/       # Pages
│   ├── App.jsx
│   └── main.jsx
│
├── public/
└── vite.config.js
```

---

## Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/rakesh15092002/hospital_voice_assistent.git
cd hospital_voice_assistent
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## Environment Variables

Create a `.env` file in the backend directory:

```env
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_secret
LIVEKIT_URL=your_livekit_url
FRONTEND_URL=http://localhost:5173
```

---

## Workflow

1. User interacts through the frontend using voice  
2. LiveKit establishes a real-time voice connection  
3. Voice input is processed by the voice agent  
4. The agent communicates with FastAPI APIs  
5. Backend processes requests (appointments, doctor data)  
6. Response is returned as voice output  

---

## Key Functionalities

- Voice command processing  
- Automatic session creation for voice agent  
- Appointment booking and confirmation flow  
- Modular backend architecture  
- CORS handling for multi-origin deployment  

---

## Common Issues & Fixes

| Issue              | Solution                                  |
|-------------------|-------------------------------------------|
| CORS Error        | Add frontend URL in backend CORS config   |
| 403 Error         | Verify API keys and authentication tokens |
| Voice not working | Check LiveKit configuration               |
| Deployment issues | Verify environment variables              |

---

## Deployment

### Backend (Railway)
- Uses `railway.json`  
- Configure environment variables in dashboard  

### Frontend (Vercel)
- Uses `vercel.json`  
- Set API base URL in environment variables  

---

## Future Improvements

- Multi-language voice support  
- AI-based doctor recommendation  
- Patient history tracking  
- WhatsApp / chat integration  

---

## Author

**Rakesh Maurya**  
MERN Stack Developer  
Exploring AI and Voice Systems  

---

## Support

If you find this project useful, consider giving it a ⭐ on GitHub.
