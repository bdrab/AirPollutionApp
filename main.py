from secrets_db import POSTGRESQL_LOGIN, POSTGRESQL_PASS, POSTGRESQL_SERVER, POSTGRESQL_DB, APP_SECRET_KEY
from forms import LoginForm, RegisterForm

import datetime
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from werkzeug.security import generate_password_hash, check_password_hash
import uvicorn

from flask import Flask, render_template, url_for, redirect
from flask_login import UserMixin, current_user, login_user, logout_user, LoginManager, login_required
from flask_bootstrap import Bootstrap

from sqlalchemy import create_engine, Float, Column, Integer, DateTime, String, JSON
from sqlalchemy.orm import declarative_base, load_only, sessionmaker


engine = create_engine(f'postgresql://{POSTGRESQL_LOGIN}:{POSTGRESQL_PASS}@{POSTGRESQL_SERVER}/{POSTGRESQL_DB}',
                       echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class AirPollutionData(Base):
    __tablename__ = 'air_pollution_app_data'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    temperature = Column(Float)
    pressure = Column(Float)
    humidity = Column(Float)
    pm1 = Column(Float)
    pm25 = Column(Float)
    pm10 = Column(Float)


class AirPollutionSensor(Base):
    __tablename__ = 'air_pollution_app_sensor'
    id = Column(Integer, primary_key=True)
    data = Column(String)


class AirPollutionUser(UserMixin, Base):
    __tablename__ = 'air_pollution_app_user'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    username = Column(String)
    auth_key = Column(String)


Base.metadata.create_all(engine)


class Item(BaseModel):
    time: datetime.datetime
    data: dict
    email: str
    auth_key: str


description = """AirPollutionApp helps you get air pollution data from sensor based in Cracow/Poland."""


app = FastAPI(docs_url=None, description=description, title="AirPollutionApp")
flask_app = Flask(__name__)
flask_app.config['SECRET_KEY'] = APP_SECRET_KEY
Bootstrap(flask_app)
app.mount("/portal/", WSGIMiddleware(flask_app))
app.mount("/static", StaticFiles(directory="static"), name="static")


login_manager = LoginManager()
login_manager.init_app(flask_app)


@login_manager.user_loader
def load_user(user_id):
    return session.query(AirPollutionUser).get(user_id)


@flask_app.route("/")
def main():
    """
        Flask main page
    """
    return render_template("index.html", user=current_user)


@flask_app.route("/maps")
@login_required
def maps():
    """
        Page contains page with all sensors
    """
    markers = [{'lat': 50.054045434391156, 'lon': 19.935247879895858, 'popup': "PM1: 10 ,PM2.5: 23, PM10: 45"}]

    return render_template("map.html", markers=markers, user=current_user)


@flask_app.route("/register", methods=["GET", "POST"])
def register_func():
    form = RegisterForm()
    if form.validate_on_submit():
        user_email = form.email.data
        if session.query(AirPollutionUser).filter_by(email=form.email.data).first():
            return redirect(url_for("login_func"))
        new_user = AirPollutionUser(
            email=user_email,
            username=form.username.data,
            auth_key=generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        )
        session.add(new_user)
        session.commit()
        login_user(new_user)
        return redirect(url_for("main"))
    return render_template("register.html", form=form, user=current_user)


@flask_app.route("/login", methods=["GET", "POST"])
def login_func():
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(AirPollutionUser).filter_by(email=form.email.data).first()
        if not user:
            return redirect(url_for("register_func"))
        elif not check_password_hash(user.auth_key, form.password.data):
            return redirect(url_for("login_func"))
        else:
            login_user(user)
            return redirect(url_for("main"))
    return render_template("login.html", form=form, user=current_user)


@flask_app.route("/logout")
def logout_func():
    logout_user()
    return redirect(url_for("main"))


@app.get("/", include_in_schema=False)
def root():
    """
        Redirect to Flask Main Page
    """
    return RedirectResponse("/portal")


@app.get("/docs", include_in_schema=False)
def swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="AirPollutionApp",
        swagger_favicon_url="/static/favicon.ico",
    )


@app.get("/get-data/")
async def download(period: int, auth_key: str, number: int = None, data_required: str = None):
    """
        Return <number> record from database
    """

    authenticated = False

    for record in session.query(AirPollutionUser).all():
        if check_password_hash(record.auth_key, auth_key):
            authenticated = True

    if not authenticated:
        raise HTTPException(status_code=401, detail="User does not exist")
    try:
        today = datetime.datetime.now()
        older_than = today - datetime.timedelta(days=period)
        data = session.query(AirPollutionData).filter(AirPollutionData.time > older_than).options(load_only(*[data_required])).all()
    except TypeError:
        raise HTTPException(status_code=500, detail="Internal error, data not provided.")

    return data


@app.post("/send-data", status_code=201)
async def upload(item: Item):
    """
        Upload data if user provides correct authentication key.
    """

    authenticated = False

    for record in session.query(AirPollutionUser).all():
        if check_password_hash(record.auth_key, item.auth_key):
            authenticated = True

    if not authenticated:
        raise HTTPException(status_code=401, detail="User does not exist")

    try:
        new_device = AirPollutionData(time=item.time,
                                      temperature=item.data["temperature"],
                                      pressure=item.data["pressure"],
                                      humidity=item.data["humidity"],
                                      pm1=item.data["pm1"],
                                      pm25=item.data["pm2.5"],
                                      pm10=item.data["pm10"])
        session.add(new_device)
        session.commit()
    except TypeError:
        raise HTTPException(status_code=500, detail="Internal error, not added")

    return {"detail": "User authenticated. Data added into db."}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
