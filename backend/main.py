from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import jwt

from database import users, students
from auth import hash_password, verify_password, create_token

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

SECRET = "secret123"


def verify_token(token=Depends(security)):
    payload = jwt.decode(token.credentials, SECRET, algorithms=["HS256"])
    return payload


@app.post("/signup")
def signup(user: dict):

    if users.find_one({"email": user["email"]}):
        raise HTTPException(400, "User already exists")

    user["password"] = hash_password(user["password"])

    users.insert_one(user)

    return {"message": "User created"}


@app.post("/login")
def login(data: dict):

    user = users.find_one({"email": data["email"]})

    if not user or not verify_password(data["password"], user["password"]):
        raise HTTPException(401, "Invalid credentials")

    token = create_token({
        "id": str(user["_id"]),
        "role": user["role"]
    })

    return {"token": token}


@app.get("/students")
def get_students(user=Depends(verify_token)):

    data = list(students.find())

    for student in data:
        student["_id"] = str(student["_id"])

    return data


@app.put("/students/{name}")
def update_student(name: str, body: dict, user=Depends(verify_token)):

    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin only")

    result = students.update_one(
        {"name": name},
        {"$set": body}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student updated successfully"}