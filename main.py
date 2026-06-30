
from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import numpy as np
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse

app=FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

model=joblib.load('student_perform.pkl')

class StudentData(BaseModel):
    hours_studied: float
    attendance: float
    sleep_hours: float
    Parental_Education: int
    Extra_Activities: int
    Previous_Score: float



@app.get('/')
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"prediction": None})

@app.post('/')
def get_prediction(
    request: Request,
    hours_studied: float = Form(...),
    attendance: float = Form(...),
    sleep_hours: float = Form(...),
    Parental_Education: int = Form(...),
    Extra_Activities: int = Form(...),
    Previous_Score: float = Form(...)
):
    # Create StudentData instance
    data = StudentData(
        hours_studied=hours_studied,
        attendance=attendance,
        sleep_hours=sleep_hours,
        Parental_Education=Parental_Education,
        Extra_Activities=Extra_Activities,
        Previous_Score=Previous_Score
    )
    
    # Make prediction
    features = np.array(([data.hours_studied, data.attendance, data.sleep_hours, data.Parental_Education, data.Extra_Activities, data.Previous_Score])).reshape(1,-1)
    prediction = model.predict(features)
    result = 'Pass' if prediction[0] == 1 else 'Fail'
    advice = "Keep up the good work!" if result == 'Pass' else "Consider improving study habits and attendance."
    
    # Return template with prediction result
    return templates.TemplateResponse(request, "index.html", {
        "prediction": result,
        "advice": advice,
        "hours_studied": hours_studied,
        "attendance": attendance,
        "sleep_hours": sleep_hours,
        "Parental_Education": Parental_Education,
        "Extra_Activities": Extra_Activities,
        "Previous_Score": Previous_Score
    })
