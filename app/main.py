from fastapi import FastAPI
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from sqlalchemy.sql import select,text
import json
from fastapi.encoders import jsonable_encoder



app = FastAPI()

DATABASE_URL = "mysql+pymysql://root:mypassword@ai4europe-db:3306/mydb"
engine = sa.create_engine(DATABASE_URL)
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)


inspector = inspect(engine)
tables = inspector.get_table_names()




@app.get("/ai_assets/{id}")
async def get_ai_asset(id):

    """
    id: ID for the ai_asset that will be fetched
    """

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
        ai_asset
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
        ai_asset
        ).all()

    return q





@app.get("/organisation/{id}")
async def get_organisation(id):
    """
    id: ID for the organisation that will be fetched
    """

    organisation = sa.Table('organisation', sa.MetaData(), autoload_with=engine)

    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine)
    organisation_has_technical_category = sa.Table('organisation_has_technical_category',sa.MetaData(), autoload_with=engine)

    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine)
    organisation_has_tag = sa.Table('organisation_has_tag',sa.MetaData(), autoload_with=engine)

    organisation_review = sa.Table('organisation_review',sa.MetaData(), autoload_with=engine)

    q = session.query(
        organisation
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
        organisation
    ).all()
   
    return q







@app.get("/case_study/{id}")
async def get_case_study(id):
    """
    id: ID for the case_study that will be fetched
    """


    case_study = sa.Table('case_study', sa.MetaData(), autoload_with=engine)

    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine)
    case_study_has_technical_category = sa.Table('case_study_has_technical_category',sa.MetaData(), autoload_with=engine)

    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine)
    case_study_has_business_category = sa.Table('case_study_has_business_category',sa.MetaData(), autoload_with=engine)

    case_study_review = sa.Table('case_study_review',sa.MetaData(), autoload_with=engine)

    q = session.query(
        case_study
        
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



@app.get("/case_study/")
async def get_all_case_studies():

    case_study = sa.Table('case_study', sa.MetaData(), autoload_with=engine)

    q = session.query(
        case_study
        
    ).all()
    return q


@app.get("/educational_resource/{id}")
async def get_educational_resource(id):
    """
    id: ID for the educational_resource that will be fetched
    """

    educational_resource = sa.Table('educational_resource', sa.MetaData(), autoload_with=engine)
    

    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine)
    educational_resource_has_business_category = sa.Table('educational_resource_has_business_category',sa.MetaData(), autoload_with=engine)
    
    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine)
    educational_resource_has_technical_category = sa.Table('educational_resource_has_technical_category',sa.MetaData(), autoload_with=engine)

    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine)
    educational_resource_has_tag = sa.Table('educational_resource_has_tag',sa.MetaData(), autoload_with=engine)

    educational_resource_review = sa.Table('educational_resource_review',sa.MetaData(), autoload_with=engine)

    q = session.query(
        educational_resource

        ).filter(
            educational_resource.c.id == id
        ).first()

    r = session.query(
        educational_resource_review.c.comment
    ).filter(
        educational_resource_review.c.educational_resource_id == id
    ).all()


    b = session.query(
        business_category.c.category
    ).join(
        educational_resource_has_business_category,educational_resource_has_business_category.c.educational_resource_id == id
    ).filter(
        business_category.c.id == educational_resource_has_business_category.c.business_category_id
    ).all()


    t = session.query(
        technical_category.c.category
    ).join(
        educational_resource_has_technical_category,educational_resource_has_technical_category.c.educational_resource_id == id
    ).filter(
        technical_category.c.id == educational_resource_has_technical_category.c.technical_category_id
    ).all()

    t1 = session.query(
        tag.c.tag
    ).join(
        educational_resource_has_tag,educational_resource_has_tag.c.educational_resource_id == id
    ).filter(
        tag.c.id == educational_resource_has_tag.c.tag_id
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



@app.get("/educational_resource/")
async def get_all_educational_resources():

    educational_resource = sa.Table('educational_resource', sa.MetaData(), autoload_with=engine)

    q = session.query(
        educational_resource
        ).all()

    return q



@app.get("/event/{id}")
async def get_event(id):
    """
    id: ID for the event that will be fetched
    """

    event = sa.Table('event', sa.MetaData(), autoload_with=engine)


    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine)
    event_has_business_category = sa.Table('event_has_business_category',sa.MetaData(), autoload_with=engine)

    

    q = session.query(
        event
        
    ).filter(
        event.c.id == id
    ).first()
   
  

    b = session.query(
        business_category.c.category
    ).join(
        event_has_business_category,event_has_business_category.c.event_id == id
    ).filter(
        business_category.c.id == event_has_business_category.c.business_category_id
    ).all()


    business_categories = []
    for x in b:
        business_categories.append(x[0])

   
  
    result = {}
    result = dict(q)
    result["business_categories"] = business_categories  

    return result


@app.get("/event/")
async def get_all_events(id):

    event = sa.Table('event', sa.MetaData(), autoload_with=engine)

    q = session.query(
        event
        
    ).all()
   
    return q



@app.get("/news/{id}")
async def get_news(id):
    """
    id: ID for news that will be fetched
    """

    news = sa.Table('news', sa.MetaData(), autoload_with=engine)
    

    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine)
    news_has_business_category = sa.Table('news_has_business_category',sa.MetaData(), autoload_with=engine)
    
    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine)
    news_has_tag = sa.Table('news_has_tag',sa.MetaData(), autoload_with=engine)

    news_category = sa.Table('news_category',sa.MetaData(), autoload_with=engine)
    news_has_news_category = sa.Table('news_has_news_category',sa.MetaData(), autoload_with=engine)

    q = session.query(
        news

        ).filter(
            news.c.id == id
        ).first()




    b = session.query(
        business_category.c.category
    ).join(
        news_has_business_category,news_has_business_category.c.news_id == id
    ).filter(
        business_category.c.id == news_has_business_category.c.business_category_id
    ).all()



    t = session.query(
        tag.c.tag
    ).join(
        news_has_tag,news_has_tag.c.news_id == id
    ).filter(
        tag.c.id == news_has_tag.c.tag_id
    ).all()


    n = session.query(
        news_category.c.category
    ).join(
        news_has_news_category,news_has_news_category.c.news_id == id
    ).filter(
        news_category.c.id == news_has_news_category.c.news_category_id
    ).all()

    
    business_categories = []
    for x in b:
        business_categories.append(x[0])


    tags = []
    for x in t:
        tags.append(x[0])

    news_categories = []
    for x in t:
        news_categories.append(x[0])
    
    
    result = {}
    result = dict(q)
    result["tags"] = tags
    result["business_categories"] = business_categories
    result["news_categories"] = news_categories

    
    return result



@app.get("/news/")
async def get_all_news(id):
    
    news = sa.Table('news', sa.MetaData(), autoload_with=engine)

    q = session.query(
        news
        ).all()
    
    return q


@app.get("/open_call/{id}")
async def get_open_call(id):
    """
    id: ID for open_call that will be fetched
    """

    open_call = sa.Table('open_call', sa.MetaData(), autoload_with=engine)
    

    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine)
    open_call_has_business_category = sa.Table('open_call_has_business_category',sa.MetaData(), autoload_with=engine)
    
    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine)
    open_call_has_tag = sa.Table('open_call_has_tag',sa.MetaData(), autoload_with=engine)

    target_application = sa.Table('target_application',sa.MetaData(), autoload_with=engine)
    open_call_has_target_application = sa.Table('open_call_has_target_application',sa.MetaData(), autoload_with=engine)

    q = session.query(
        open_call
        ).filter(
            open_call.c.id == id
        ).first()




    b = session.query(
        business_category.c.category
    ).join(
        open_call_has_business_category,open_call_has_business_category.c.open_call_id == id
    ).filter(
        business_category.c.id == open_call_has_business_category.c.business_category_id
    ).all()



    t = session.query(
        tag.c.tag
    ).join(
        open_call_has_tag,open_call_has_tag.c.open_call_id == id
    ).filter(
        tag.c.id == open_call_has_tag.c.tag_id
    ).all()


    a = session.query(
        target_application.c.application    
    ).join(
        open_call_has_target_application,open_call_has_target_application.c.open_call_id == id
    ).filter(
        target_application.c.id == open_call_has_target_application.c.target_application_id
    ).all()

    
    business_categories = []
    for x in b:
        business_categories.append(x[0])


    tags = []
    for x in t:
        tags.append(x[0])

    target_applications = []
    for x in a:
        target_applications.append(x[0])
    
    
    result = {}
    result = dict(q)
    result["tags"] = tags
    result["business_categories"] = business_categories
    result["target_applications"] = target_applications

    
    return result



@app.get("/open_call/")
async def get_open_call(id):


    open_call = sa.Table('open_call', sa.MetaData(), autoload_with=engine)
    

    q = session.query(
        open_call
        ).all()

    return q