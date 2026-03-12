# Full Stack Student Management System

## Tech Stack
Frontend: React (Vite)  
Backend: FastAPI  
Database: MongoDB Atlas  
Authentication: JWT

## Features
- Login with JWT authentication
- Role based access control
- Normal users can view students
- Admin can update student data

## Run Backend

cd backend  
pip install -r requirements.txt  
uvicorn main:app --reload

Backend runs at:
http://127.0.0.1:8000

## Run Frontend

cd frontend  
npm install  
npm run dev

Frontend runs at:
http://localhost:5173

## API Docs

Swagger UI:
http://127.0.0.1:8000/docs