from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer
from playwright.sync_api import sync_playwright
import base64
from jose import jwt

from database import users, students
from auth import hash_password, verify_password, create_token

app = FastAPI()

# CORS configuration
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
        raise HTTPException(status_code=400, detail="User already exists")

    user["password"] = hash_password(user["password"])

    users.insert_one(user)

    return {"message": "User created"}


@app.post("/login")
def login(data: dict):

    user = users.find_one({"email": data["email"]})

    if not user or not verify_password(data["password"], user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

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


@app.get("/screenshot")
def capture(url: str):

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
            )

            context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            )

            page = context.new_page()

            # consistent screenshot size
            page.set_viewport_size({"width": 1280, "height": 800})

            # safer loading for heavy JS sites
            page.goto(url, wait_until="domcontentloaded", timeout=60000)

            # allow dynamic content to load
            page.wait_for_timeout(3000)

            screenshot = page.screenshot(full_page=True)

            browser.close()

        encoded = base64.b64encode(screenshot).decode()

        return {"image": encoded}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))