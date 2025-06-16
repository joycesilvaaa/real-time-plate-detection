from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

conn = sqlite3.connect("database.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS placas
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              placa TEXT,
              data_hora TEXT,
              confianca REAL)''')
conn.commit()
conn.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT placa, data_hora, confianca FROM placas ORDER BY id DESC LIMIT 10")
    placas = c.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "placas": placas})

@app.get("/api/ultimas")
def ultimas():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT placa, data_hora, confianca FROM placas ORDER BY id DESC LIMIT 10")
    placas = c.fetchall()
    conn.close()
    return {"placas": [
        {"placa": p, "data_hora": d, "confianca": c} for p, d, c in placas
    ]}

@app.post("/api/inserir")
def inserir(placa: str = Form(...), confianca: float = Form(...)):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO placas (placa, data_hora, confianca) VALUES (?, ?, ?)", (placa, data_hora, confianca))
    conn.commit()
    conn.close()
    return {"status": "ok"}