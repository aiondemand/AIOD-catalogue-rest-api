from fastapi import FastAPI
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from sqlalchemy.sql import select,text
import json
from fastapi.encoders import jsonable_encoder



app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:mypassword@172.17.0.2:3306/mydb"
engine = sa.create_engine(DATABASE_URL)
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)


inspector = inspect(engine)
tables = inspector.get_table_names()


@app.get("/ai_assets/{id}")
async def get_ai_assets(id):

    ai_asset = sa.Table('ai_asset', sa.MetaData(), autoload_with=engine)
    organisation = sa.Table('organisation', sa.MetaData(), autoload_with=engine)

    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine)
    ai_asset_has_business_category = sa.Table('ai_asset_has_business_category',sa.MetaData(), autoload_with=engine)
    
    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine)
    ai_asset_has_technical_category = sa.Table('ai_asset_has_technical_category',sa.MetaData(), autoload_with=engine)

    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine)
    ai_asset_has_tag = sa.Table('ai_asset_has_tag',sa.MetaData(), autoload_with=engine)

    ai_asset_review = sa.Table('ai_asset_review',sa.MetaData(), autoload_with=engine)

    q = session.query(
        ai_asset.c.title,
        ai_asset.c.asset_type,
        ai_asset.c.main_characteristic,
        ai_asset.c.documentation,
        ai_asset.c.gdpr_requirements,
        ai_asset.c.trustworthy_ai,
        ai_asset.c.license,
        ai_asset.c.research_areas,
        ai_asset.c.website,
        ).filter(
            ai_asset.c.id == id
        ).first()

    r = session.query(
        ai_asset_review.c.comment
    ).filter(
        ai_asset_review.c.ai_asset_id == id, ai_asset_review.c.ai_asset_version == ai_asset.c.version
    ).all()


    b = session.query(
        business_category.c.category
    ).join(
        ai_asset_has_business_category,ai_asset_has_business_category.c.ai_asset_id == id
    ).filter(
        business_category.c.id == ai_asset_has_business_category.c.business_category_id, ai_asset_has_business_category.c.ai_asset_version == ai_asset.c.version
    ).all()


    t = session.query(
        technical_category.c.category
    ).join(
        ai_asset_has_technical_category,ai_asset_has_technical_category.c.ai_asset_id == id
    ).filter(
        technical_category.c.id == ai_asset_has_technical_category.c.technical_category_id, ai_asset_has_technical_category.c.ai_asset_version == ai_asset.c.version 
    ).all()

    t1 = session.query(
        tag.c.tag
    ).join(
        ai_asset_has_tag,ai_asset_has_tag.c.ai_asset_id == id
    ).filter(
        tag.c.id == ai_asset_has_tag.c.tag_id,ai_asset_has_tag.c.ai_asset_version == ai_asset.c.version 
    ).all()

    reviews = []
    for x in r:
        reviews.append(x[0])

    business_categories = []
    for x in b:
        business_categories.append(x[0])

    technical_categories = []
    for x in t:
        technical_categories.append(x[0])

    tags = []
    for x in t1:
        tags.append(x[0])
    
    
    result = {}
    result = dict(q)
    result["reviews"] = reviews
    result["tags"] = tags
    result["business_categories"] = business_categories
    result["technical_categories"] = technical_categories
    
    return result


@app.get("/ai_assets/")
async def get_all_ai_assets():

    ai_asset = sa.Table('ai_asset', sa.MetaData(), autoload_with=engine)
    
    q = session.query(
        ai_asset.c.title,
        ai_asset.c.asset_type,
        ai_asset.c.main_characteristic,
        ai_asset.c.documentation,
        ai_asset.c.gdpr_requirements,
        ai_asset.c.trustworthy_ai,
        ai_asset.c.license,
        ai_asset.c.research_areas,
        ai_asset.c.website,
        ai_asset.c.version
        ).all()

    return q





@app.get("/organisation/{id}")
async def get_organisation(id):

    organisation = sa.Table('organisation', sa.MetaData(), autoload_with=engine)

    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine)
    organisation_has_technical_category = sa.Table('organisation_has_technical_category',sa.MetaData(), autoload_with=engine)

    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine)
    organisation_has_tag = sa.Table('organisation_has_tag',sa.MetaData(), autoload_with=engine)

    organisation_review = sa.Table('organisation_review',sa.MetaData(), autoload_with=engine)

    q = session.query(
        organisation.c.title,
        organisation.c.address,
        organisation.c.connection_to_ai,
        organisation.c.body,
        organisation.c.email,
        organisation.c.organisation_type,
        organisation.c.relation_to_organisation,
        organisation.c.website,
    ).filter(
        organisation.c.id == id
    ).first()
   
    r = session.query(
        organisation_review.c.comment
    ).filter(
        organisation_review.c.organisation_id == id
    ).all()

    t = session.query(
        technical_category.c.category
    ).join(
        organisation_has_technical_category,organisation_has_technical_category.c.organisation_id == id
    ).filter(
        technical_category.c.id == organisation_has_technical_category.c.technical_category_id
    ).all()

    t1 = session.query(
        tag.c.tag
    ).join(
        organisation_has_tag,organisation_has_tag.c.organisation_id == id
    ).filter(
        tag.c.id == organisation_has_tag.c.tag_id
    ).all()    
    
    reviews = []
    for x in r:
        reviews.append(x[0])


    technical_categories = []
    for x in t:
        technical_categories.append(x[0])

    tags = []
    for x in t1:
        tags.append(x[0])
    
    
    result = {}
    result = dict(q)
    result["reviews"] = reviews
    result["tags"] = tags
    result["technical_categories"] = technical_categories  

    return result



@app.get("/organisation")
async def get_all_organisations():

    organisation = sa.Table('organisation', sa.MetaData(), autoload_with=engine)

    q = session.query(
        organisation.c.title,
        organisation.c.address,
        organisation.c.connection_to_ai,
        organisation.c.body,
        organisation.c.email,
        organisation.c.organisation_type,
        organisation.c.relation_to_organisation,
        organisation.c.website,
    ).all()
   
    return q







@app.get("/case_study/{id}")
async def get_case_study(id):

    case_study = sa.Table('case_study', sa.MetaData(), autoload_with=engine)

    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine)
    case_study_has_technical_category = sa.Table('case_study_has_technical_category',sa.MetaData(), autoload_with=engine)

    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine)
    case_study_has_business_category = sa.Table('case_study_has_business_category',sa.MetaData(), autoload_with=engine)

    case_study_review = sa.Table('case_study_review',sa.MetaData(), autoload_with=engine)

    q = session.query(
        case_study.c.title,
        case_study.c.body,
        case_study.c.email,
        case_study.c.website
        
    ).filter(
        case_study.c.id == id
    ).first()
   
    r = session.query(
        case_study_review.c.comment
    ).filter(
        case_study_review.c.case_study_id == id
    ).all()

    b = session.query(
        business_category.c.category
    ).join(
        case_study_has_business_category,case_study_has_business_category.c.case_study_id == id
    ).filter(
        business_category.c.id == case_study_has_business_category.c.business_category_id
    ).all()


    t = session.query(
        technical_category.c.category
    ).join(
        case_study_has_technical_category,case_study_has_technical_category.c.case_study_id == id
    ).filter(
        technical_category.c.id == case_study_has_technical_category.c.technical_category_id
    ).all()

   
    
    reviews = []
    for x in r:
        reviews.append(x[0])
  
    business_categories = []
    for x in b:
        business_categories.append(x[0])

    technical_categories = []
    for x in t:
        technical_categories.append(x[0])

  
    result = {}
    result = dict(q)
    result["reviews"] = reviews
    result["business_categories"] = business_categories  
    result["technical_categories"] = technical_categories  

    return result



@app.get("/case_study/{id}")
async def get_case_study(id):

    case_study = sa.Table('case_study', sa.MetaData(), autoload_with=engine)

    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine)
    case_study_has_technical_category = sa.Table('case_study_has_technical_category',sa.MetaData(), autoload_with=engine)

    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine)
    case_study_has_business_category = sa.Table('case_study_has_business_category',sa.MetaData(), autoload_with=engine)

    case_study_review = sa.Table('case_study_review',sa.MetaData(), autoload_with=engine)

    q = session.query(
        case_study.c.title,
        case_study.c.body,
        case_study.c.email,
        case_study.c.website
        
    ).all()
    return q