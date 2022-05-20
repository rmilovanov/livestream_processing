from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from flask import render_template, Response

from models import StreamGenerator

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    # res = StreamingResponse()
    # return StreamingResponse(StreamGenerator.gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return StreamingResponse(StreamGenerator.gen_frames(), media_type="multipart/x-mixed-replace; boundary=frame")


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    """Video streaming home page."""
    return templates.TemplateResponse('index.html', {"request": request})
