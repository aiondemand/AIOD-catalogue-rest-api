from fastapi import FastAPI
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from sqlalchemy.sql import select,text
import json
from fastapi.encoders import jsonable_encoder



app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:mypassword@172.17.0.3:3306/mydb"
engine = sa.create_engine(DATABASE_URL)
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)


inspector = inspect(engine)
tables = inspector.get_table_names()


@app.get("/dummy")
def dummy():
   return {"message": "Hello world"}