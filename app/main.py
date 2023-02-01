from grp import struct_group
from os import stat_result
from pyexpat import model
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
from sqlalchemy.sql import select,text
import json
from fastapi.encoders import jsonable_encoder



app = FastAPI()

# DATABASE_URL = "mysql+pymysql://root:JNqgDYAIMPaPCF89Qsfl@ai4europe-db:3306/mydb"
DATABASE_URL = "mysql+pymysql://root:mypassword@172.17.0.2:3306/mydb" 
engine = sa.create_engine(DATABASE_URL)
session = Session(engine)

Base = automap_base()
Base.prepare(engine, reflect=True)


inspector = inspect(engine)
tables = inspector.get_table_names()


    

class OrganisationModel(BaseModel):
    title: str
    relation_to_organisation: bool = False
    connection_to_ai: str = None
    organisation_type: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    technical_categories: Optional[list] = None
    business_categories: Optional[list] = None
    review_comments: Optional[list] = None


class AiAssetModel(BaseModel):
    title: str
    summary: str
    main_characteristic: str
    organisation: str 
    asset_type: Optional[str] = None
    technical_categories: Optional[list] = None
    business_categories: Optional[list] = None
    research_areas: Optional[str] = None
    license: Optional[str] = None
    other_license: Optional[str] = None
    tags: Optional[list] = None
    website: Optional[str] = None
    contact_details: Optional[str] = None
    documentation: Optional[str] = None
    gdpr_requirements: Optional[str] = None
    trustworthy_ai: Optional[str] = None
    trustworthy_ai_assessment: Optional[str] = None
    review_comments: Optional[list] = None



class CaseStudyModel(BaseModel):
    title: str
    summary: str
    organisation: str
    email: Optional[str] = None
    website: Optional[str] = None
    technical_categories: Optional[list] = None
    business_categories: Optional[list] = None
    review_comments: Optional[list] = None  



class EventModel(BaseModel):
    title: str
    summary: str
    description: str
    start_date: str
    end_date: str     
    date_of_event: Optional[str] = None
    email: Optional[str] = None
    registration_link: Optional[str] = None
    event_type: Optional[str] = None
    business_categories: Optional[list] = None



class NewsModel(BaseModel):
    title: str
    body: str
    source: Optional[str] = None
    tags: Optional[list] = None
    news_categories: Optional[list] = None
    business_categories: Optional[list] = None
    review_comments: Optional[list] = None



class EducationalResourceModel(BaseModel):
	title: str
	organisation: str 
	contact_details: Optional[str] = None
	country: Optional[str] = None
	credits: Optional[str] = None
	duration_minutes_and_hours: Optional[str] = None
	educational_type: Optional[str] = None
	language: Optional[str] = None
	educational_level: Optional[str] = None
	number_of_weeks: Optional[str] = None
	prerequisites: Optional[str] = None
	body: Optional[str] = None
	target_audience: Optional[str] = None
	duration_years: Optional[str] = None
	website: Optional[str] = None
	business_categories: Optional[list] = None
	technical_categories: Optional[list] = None
	tags: Optional[list] = None
	reviews: Optional[list] = None



class OpenCallModel(BaseModel):
    title: str
    date: str
    body: str
    start_date: str
    end_date: str  
    source: Optional[str] = None
    business_categories: Optional[list] = None
    review_comments: Optional[list] = None
    tags: Optional[list] = None
    target_applications: Optional[list] = None


class ProjectModel(BaseModel):
    acronym: str
    title: str
    body: str
    links: str
    project_type: Optional[str] = None
    funding_call: Optional[str] = None
    business_categories: Optional[list] = None
    case_studies: Optional[list] = None
    educational_resources: Optional[list] = None
    events: Optional[list] = None
    news: Optional[list] = None
    open_calls: Optional[list] = None
    organisations: Optional[list] = None
    reviews: Optional[list] = None



@app.post("/organisation/")
async def insert_organisation(org: OrganisationModel):

    Organisation = Base.classes.organisation

    
    author_id = 1
    drupal_id = 1
    date = datetime.today().strftime('%Y-%m-%d') 
    new_organisation = Organisation(
        title = org.title,
        date = date,
        author_id = author_id,
        drupal_id = drupal_id,
        relation_to_organisation = org.relation_to_organisation,
        organisation_type = org.organisation_type, 
        connection_to_ai = org.relation_to_organisation,
        summary = org.summary,
        description = org.description,
        email = org.email
    )
    session.add(new_organisation)
    session.flush()
    session.refresh(new_organisation)
    new_id = new_organisation.id

    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine) 
    for category in org.business_categories:
        q = session.query(
            business_category.c.id
            ).filter(
                business_category.c.category == category
            ).first()
        if q is not None:
            organisation_has_business_category = sa.Table('organisation_has_business_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "organisation_id": new_id,
                "business_category_id": q[0]
            }
            stmt = sa.insert(organisation_has_business_category).values(vals)
            session.execute(stmt)        

    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine) 
    for category in org.technical_categories:
        q = session.query(
            technical_category.c.id
            ).filter(
                technical_category.c.category == category
            ).first()
        if q is not None:
            organisation_has_technical_category = sa.Table('organisation_has_technical_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "organisation_id": new_id,
                "technical_category_id": q[0]
            }
            stmt = sa.insert(organisation_has_technical_category).values(vals)
            session.execute(stmt)



    for review in org.review_comments:
        organisation_review = sa.Table('organisation_review',sa.MetaData(), autoload_with=engine)
        vals = {
            "organisation_id": new_id,
            "comment": review
        }
        stmt = sa.insert(organisation_review).values(vals)
        session.execute(stmt)

    session.commit()
    return  {"message": "OK"}


@app.post("/ai_asset/")
async def insert_ai_asset(ai_asset: AiAssetModel):
    AiAsset = Base.classes.ai_asset
    


    organisation = sa.Table('organisation',sa.MetaData(), autoload_with=engine) 
    q = session.query(
        organisation.c.id
        ).filter(
            organisation.c.title == ai_asset.organisation
        ).first()
    
    organisation_id = 0
    if q is not None:
        organisation_id = q[0]


    author_id = 1
    drupal_id = 1
    version = 1
    under_review = False
    date = datetime.today().strftime('%Y-%m-%d') 
    new_ai_asset = AiAsset(
        version = version,
        author_id = author_id,
        drupal_id = drupal_id,
        date = date,
        organisation_id = organisation_id,
        title = ai_asset.title,
        under_review = under_review,
        asset_type = ai_asset.asset_type,
        contact_details = ai_asset.contact_details,
        documentation = ai_asset.documentation,
        gdpr_requirements = ai_asset.gdpr_requirements,
        license = ai_asset.license,
        other_licence = ai_asset.other_license,
        research_areas = ai_asset.research_areas,
        trustworthy_ai = ai_asset.trustworthy_ai,
        trustworthy_ai_assessment = ai_asset.trustworthy_ai_assessment,
        website = ai_asset.website

    )

    session.add(new_ai_asset)
    session.flush()
    session.refresh(new_ai_asset)
    new_id = new_ai_asset.id


    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine) 
    for category in ai_asset.business_categories:
        q = session.query(
            business_category.c.id
            ).filter(
                business_category.c.category == category
            ).first()
        if q is not None:
            ai_asset_has_business_category = sa.Table('ai_asset_has_business_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "ai_asset_id": new_id,
                "ai_asset_version": ai_asset.version,
                "business_category_id": q[0]
            }
            stmt = sa.insert(ai_asset_has_business_category).values(vals)
            session.execute(stmt)        

    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine) 
    for category in ai_asset.technical_categories:
        q = session.query(
            technical_category.c.id
            ).filter(
                technical_category.c.category == category
            ).first()
        if q is not None:
            ai_asset_has_technical_category = sa.Table('ai_asset_has_technical_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "ai_asset_id": new_id,
                "ai_asset_version": ai_asset.version,
                "technical_category_id": q[0]
            }
            stmt = sa.insert(ai_asset_has_technical_category).values(vals)
            session.execute(stmt)

    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine) 
    for t in ai_asset.tags:
        q = session.query(
            tag.c.id
            ).filter(
                tag.c.tag == t
            ).first()
        if q is not None:
            ai_asset_has_tag = sa.Table('ai_asset_has_tag',sa.MetaData(), autoload_with=engine)
            vals = {
                "ai_asset_id": new_id,
                "ai_asset_version": ai_asset.version,
                "tag_id": q[0]
            }
            stmt = sa.insert(ai_asset_has_tag).values(vals)
            session.execute(stmt)



    for review in ai_asset.review_comments:
        ai_asset_review = sa.Table('ai_asset_review',sa.MetaData(), autoload_with=engine)
        vals = {
            "ai_asset_id": new_id,
            "comment": review
        }
        stmt = sa.insert(ai_asset_review).values(vals)
        session.execute(stmt)

    session.commit()
    return  {"message": "OK"}




@app.post("/case_study/")
async def insert_case_study(case_study: CaseStudyModel):
    CaseStudy = Base.classes.case_study
    


    organisation = sa.Table('organisation',sa.MetaData(), autoload_with=engine) 
    q = session.query(
        organisation.c.id
        ).filter(
            organisation.c.title == case_study.organisation
        ).first()
    
    organisation_id = 0
    if q is not None:
        organisation_id = q[0]


    author_id = 1
    drupal_id = 1
    version = 1
    date = datetime.today().strftime('%Y-%m-%d') 
    new_case_study = CaseStudy(
        version = version,
        author_id = author_id,
        drupal_id = drupal_id,
        date = date,
        organisation_id = organisation_id,
        title = case_study.title,
        body = case_study.body,
        email = case_study.email,
        website = case_study.website
    )

    session.add(new_case_study)
    session.flush()
    session.refresh(new_case_study)
    new_id = new_case_study.id


    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine) 
    for category in case_study.business_categories:
        q = session.query(
            business_category.c.id
            ).filter(
                business_category.c.category == category
            ).first()
        if q is not None:
            case_study_has_business_category = sa.Table('case_study_has_business_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "case_study_id": new_id,
                "business_category_id": q[0]
            }
            stmt = sa.insert(case_study_has_business_category).values(vals)
            session.execute(stmt)        

    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine) 
    for category in case_study.technical_categories:
        q = session.query(
            technical_category.c.id
            ).filter(
                technical_category.c.category == category
            ).first()
        if q is not None:
            case_study_has_technical_category = sa.Table('case_study_has_technical_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "case_study_id": new_id,
                "technical_category_id": q[0]
            }
            stmt = sa.insert(case_study_has_technical_category).values(vals)
            session.execute(stmt)

    for review in case_study.review_comments:
        case_study_review = sa.Table('case_study_review',sa.MetaData(), autoload_with=engine)
        vals = {
            "case_study_id": new_id,
            "comment": review
        }
        stmt = sa.insert(case_study_review).values(vals)
        session.execute(stmt)

    session.commit()
    return  {"message": "OK"}



@app.post("/event/")
async def insert_event(event: EventModel):
    Event = Base.classes.event

    author_id = 1
    drupal_id = 1
    date = datetime.today().strftime('%Y-%m-%d') 
    start_date = date
    end_date = date
    new_event = Event(
        author_id = author_id,
        drupal_id = drupal_id,
        date = date,
        start_date = start_date,
        end_date = end_date,
        title = event.title,
        description = event.description,
        date_of_event = event.date_of_event,
        event_type = event.event_type,
        registration_link = event.registration_link
    )

    session.add(new_event)
    session.flush()
    session.refresh(new_event)
    new_id = new_event.id


    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine) 
    for category in new_event.business_categories:
        q = session.query(
            business_category.c.id
            ).filter(
                business_category.c.category == category
            ).first()
        if q is not None:
            event_has_business_category = sa.Table('event_has_business_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "event_id": new_id,
                "business_category_id": q[0]
            }
            stmt = sa.insert(event_has_business_category).values(vals)
            session.execute(stmt)        

    session.commit()
    return  {"message": "OK"}


@app.post("/news/")
async def insert_news(news: NewsModel):
    News = Base.classes.news
    
    author_id = 1
    date = datetime.today().strftime('%Y-%m-%d') 
    new_news = News(
        author_id = author_id,
        date = date,
        body = news.body,
        title = news.title,
        source = news.source
    )

    session.add(new_news)
    session.flush()
    session.refresh(new_news)
    new_id = new_news.id


    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine) 
    for category in news.business_categories:
        q = session.query(
            business_category.c.id
            ).filter(
                business_category.c.category == category
            ).first()
        if q is not None:
            news_has_business_category = sa.Table('news_has_business_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "news_id": new_id,
                "business_category_id": q[0]
            }
            stmt = sa.insert(news_has_business_category).values(vals)
            session.execute(stmt)        

    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine) 
    for t in news.tags:
        q = session.query(
            tag.c.id
            ).filter(
                tag.c.tag == t
            ).first()
        if q is not None:
            news_has_tag = sa.Table('news_has_tag',sa.MetaData(), autoload_with=engine)
            vals = {
                "news_id": new_id,
                "tag_id": q[0]
            }
            stmt = sa.insert(news_has_tag).values(vals)
            session.execute(stmt)

    news_category = sa.Table('news_category',sa.MetaData(), autoload_with=engine) 
    for category in news.news_categories:
        q = session.query(
            news_category.c.id
            ).filter(
                news_category.c.category == category
            ).first()
        if q is not None:
            news_has_news_category = sa.Table('news_has_news_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "news_id": new_id,
                "news_category_id": q[0]
            }
            stmt = sa.insert(news_has_news_category).values(vals)
            session.execute(stmt)



    for review in news.review_comments:
        news_review = sa.Table('news_review',sa.MetaData(), autoload_with=engine)
        vals = {
            "news_id": new_id,
            "comment": review
        }
        stmt = sa.insert(news_review).values(vals)
        session.execute(stmt)

    session.commit()
    return  {"message": "OK"}



@app.post("/open_call/")
async def insert_open_call(open_call: OpenCallModel):
    OpenCall = Base.classes.open_call
    

    author_id = 1
    drupal_id = 1
    
    date = datetime.today().strftime('%Y-%m-%d') 
    start_date = date
    end_date = date
    new_open_call = OpenCall(
        author_id = author_id,
        drupal_id = drupal_id,
        date = date,
        start_date = start_date,
        end_date = end_date,
        title = open_call.title,
        source = open_call.source,
        body = open_call.body
    
    )

    session.add(new_open_call)
    session.flush()
    session.refresh(new_open_call)
    new_id = new_open_call.id


    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine) 
    for category in open_call.business_categories:
        q = session.query(
            business_category.c.id
            ).filter(
                business_category.c.category == category
            ).first()
        if q is not None:
            open_call_has_business_category = sa.Table('open_call_has_business_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "open_call_id": new_id,
                "business_category_id": q[0]
            }
            stmt = sa.insert(open_call_has_business_category).values(vals)
            session.execute(stmt)        

    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine) 
    for t in open_call.tags:
        q = session.query(
            tag.c.id
            ).filter(
                tag.c.tag == t
            ).first()
        if q is not None:
            open_call_has_tag = sa.Table('open_call_has_tag',sa.MetaData(), autoload_with=engine)
            vals = {
                "open_call_id": new_id,
                "tag_id": q[0]
            }
            stmt = sa.insert(open_call_has_tag).values(vals)
            session.execute(stmt)



    for review in open_call.review_comments:
        open_call_review = sa.Table('open_call_review',sa.MetaData(), autoload_with=engine)
        vals = {
            "open_call_id": new_id,
            "comment": review
        }
        stmt = sa.insert(open_call_review).values(vals)
        session.execute(stmt)


    target_application = sa.Table('target_application',sa.MetaData(), autoload_with=engine) 
    for application in open_call.target_applications:
        q = session.query(
            target_application.c.id
            ).filter(
                target_application.c.application == application
            ).first()
        if q is not None:
            open_call_has_target_application = sa.Table('open_call_has_target_application',sa.MetaData(), autoload_with=engine)
            vals = {
                "open_call_id": new_id,
                "target_application_id": q[0]
            }
            stmt = sa.insert(open_call_has_target_application).values(vals)
            session.execute(stmt)

    session.commit()
    return  {"message": "OK"}



@app.post("/educational_resource/")
async def insert_educational_resource(educational_resource: EducationalResourceModel):
    EducationalResource = Base.classes.educational_resource
    

    organisation = sa.Table('organisation',sa.MetaData(), autoload_with=engine) 
    q = session.query(
        organisation.c.id
        ).filter(
            organisation.c.title == educational_resource.organisation
        ).first()
    
    organisation_id = 0
    if q is not None:
        organisation_id = q[0]


    author_id = 1
    drupal_id = 1
    date = datetime.today().strftime('%Y-%m-%d') 

    new_educational_resource = EducationalResource(
        author_id = author_id,
        drupal_id = drupal_id,
        date = date,
        organisation_id = organisation_id,
        title = educational_resource.title,
        contact_details = educational_resource.contact_details,
        country = educational_resource.country,
        credits = educational_resource.credits,
        duration_minutes_and_hours = educational_resource.duration_minutes_and_hours,
        educational_type = educational_resource.educational_type,
        language = educational_resource.language,
        number_of_weeks = educational_resource.number_of_weeks,
        prerequisites = educational_resource.prerequisites,
        body = educational_resource.body,
        target_audience = educational_resource.target_audience,
        duration_years = educational_resource.duration_years,
        website = educational_resource.website

    )

    session.add(new_educational_resource)
    session.flush()
    session.refresh(new_educational_resource)
    new_id = new_educational_resource.id


    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine) 
    for category in educational_resource.business_categories:
        q = session.query(
            business_category.c.id
            ).filter(
                business_category.c.category == category
            ).first()
        if q is not None:
            educational_resource_has_business_category = sa.Table('educational_resource_has_business_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "educational_resource_id": new_id,
                "business_category_id": q[0]
            }
            stmt = sa.insert(educational_resource_has_business_category).values(vals)
            session.execute(stmt)        

    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine) 
    for category in educational_resource.technical_categories:
        q = session.query(
            technical_category.c.id
            ).filter(
                technical_category.c.category == category
            ).first()
        if q is not None:
            educational_resource_has_technical_category = sa.Table('educational_resource_has_technical_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "educational_resource_id": new_id,
                "technical_category_id": q[0]
            }
            stmt = sa.insert(educational_resource_has_technical_category).values(vals)
            session.execute(stmt)

    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine) 
    for t in educational_resource.tags:
        q = session.query(
            tag.c.id
            ).filter(
                tag.c.tag == t
            ).first()
        if q is not None:
            educational_resource_has_tag = sa.Table('educational_resource_has_tag',sa.MetaData(), autoload_with=engine)
            vals = {
                "educational_resource_id": new_id,
                "tag_id": q[0]
            }
            stmt = sa.insert(educational_resource_has_tag).values(vals)
            session.execute(stmt)


    for review in educational_resource.review_comments:
        educational_resource_review = sa.Table('educational_resource_review',sa.MetaData(), autoload_with=engine)
        vals = {
            "educational_resource_id": new_id,
            "comment": review
        }
        stmt = sa.insert(educational_resource_review).values(vals)
        session.execute(stmt)

    session.commit()
    return  {"message": "OK"}


# class ProjectModel(BaseModel):
#     acronym: str
#     title: str
#     body: str
#     links: str
#     project_type: Optional[str] = None
#     funding_call: Optional[str] = None



@app.post("/project/")
async def insert_project(project: ProjectModel):
    Project = Base.classes.project
    

    author_id = 1
    drupal_id = 1
    date = datetime.today().strftime('%Y-%m-%d') 

    new_project = Project(
        author_id = author_id,
        drupal_id = drupal_id,
        date = date,
        title = project.title,      
        body = project.body,
        project_type = project.project_type,
        funding_call = project.funding_call,
        links = project.links
    )

    session.add(new_project)
    session.flush()
    session.refresh(new_project)
    new_id = new_project.id


    business_category = sa.Table('business_category',sa.MetaData(), autoload_with=engine) 
    for category in project.business_categories:
        q = session.query(
            business_category.c.id
            ).filter(
                business_category.c.category == category
            ).first()
        if q is not None:
            project_has_business_category = sa.Table('project_has_business_category',sa.MetaData(), autoload_with=engine)
            vals = {
                "project_id": new_id,
                "business_category_id": q[0]
            }
            stmt = sa.insert(project_has_business_category).values(vals)
            session.execute(stmt)        

    case_study = sa.Table('case_study',sa.MetaData(), autoload_with=engine) 
    for id in project.case_studies:
        q = session.query(
            case_study.c.id
            ).filter(
                case_study.c.id == id
            ).first()
        if q is not None:
            project_has_case_study = sa.Table('project_has_case_study',sa.MetaData(), autoload_with=engine)
            vals = {
                "project_id": new_id,
                "case_study_id": q[0]
            }
            stmt = sa.insert(project_has_case_study).values(vals)
            session.execute(stmt)

    educational_resource = sa.Table('educational_resource',sa.MetaData(), autoload_with=engine) 
    for id in project.educational_resources:
        q = session.query(
            educational_resource.c.id
            ).filter(
                educational_resource.c.id == id
            ).first()
        if q is not None:
            project_has_educational_resource = sa.Table('project_has_educational_resource',sa.MetaData(), autoload_with=engine)
            vals = {
                "project_id": new_id,
                "educational_resource_id": q[0]
            }
            stmt = sa.insert(project_has_educational_resource).values(vals)
            session.execute(stmt)

    event = sa.Table('event',sa.MetaData(), autoload_with=engine) 
    for id in project.events:
        q = session.query(
            event.c.id
            ).filter(
                event.c.id == id
            ).first()
        if q is not None:
            project_has_event = sa.Table('project_has_event',sa.MetaData(), autoload_with=engine)
            vals = {
                "project_id": new_id,
                "event_id": q[0]
            }
            stmt = sa.insert(project_has_event).values(vals)
            session.execute(stmt)


    news = sa.Table('news',sa.MetaData(), autoload_with=engine) 
    for id in project.news:
        q = session.query(
            news.c.id
            ).filter(
                news.c.id == id
            ).first()
        if q is not None:
            project_has_news = sa.Table('project_has_news',sa.MetaData(), autoload_with=engine)
            vals = {
                "project_id": new_id,
                "news_id": q[0]
            }
            stmt = sa.insert(project_has_news).values(vals)
            session.execute(stmt)



    open_call = sa.Table('open_call',sa.MetaData(), autoload_with=engine) 
    for id in project.open_calls:
        q = session.query(
            open_call.c.id
            ).filter(
                open_call.c.id == id
            ).first()
        if q is not None:
            project_has_open_call = sa.Table('project_has_open_call',sa.MetaData(), autoload_with=engine)
            vals = {
                "project_id": new_id,
                "open_call_id": q[0]
            }
            stmt = sa.insert(project_has_open_call).values(vals)
            session.execute(stmt)

    
    organisation = sa.Table('organisation',sa.MetaData(), autoload_with=engine) 
    for id in project.organisations:
        q = session.query(
            organisation.c.id
            ).filter(
                organisation.c.id == id
            ).first()
        if q is not None:
            project_has_organisation = sa.Table('project_has_organisation',sa.MetaData(), autoload_with=engine)
            vals = {
                "project_id": new_id,
                "organisation_id": q[0]
            }
            stmt = sa.insert(project_has_organisation).values(vals)
            session.execute(stmt)


    for review in project.review_comments:
        project_review = sa.Table('project_review',sa.MetaData(), autoload_with=engine)
        vals = {
            "project_id": new_id,
            "comment": review
        }
        stmt = sa.insert(project_review).values(vals)
        session.execute(stmt)

    session.commit()
    return  {"message": "OK"}












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
async def get_all_news():
    
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
async def get_open_call():


    open_call = sa.Table('open_call', sa.MetaData(), autoload_with=engine)
    

    q = session.query(
        open_call
        ).all()

    return q




@app.get("/project/{id}")
async def get_project(id):
    """
    id: ID for project that will be fetched
    """

    project = sa.Table('project', sa.MetaData(), autoload_with=engine)
    
    ai_asset = sa.Table('ai_asset',sa.MetaData(), autoload_with=engine)
    project_has_ai_asset = sa.Table('project_has_ai_asset',sa.MetaData(), autoload_with=engine)

    case_study = sa.Table('case_study',sa.MetaData(), autoload_with=engine)
    project_has_case_study = sa.Table('project_has_case_study',sa.MetaData(), autoload_with=engine)
    
    educational_resource = sa.Table('educational_resource',sa.MetaData(), autoload_with=engine)
    project_has_educational_resource = sa.Table('project_has_educational_resource',sa.MetaData(), autoload_with=engine)

    event = sa.Table('event',sa.MetaData(), autoload_with=engine)
    project_has_event = sa.Table('project_has_event',sa.MetaData(), autoload_with=engine)

    news = sa.Table('news',sa.MetaData(), autoload_with=engine)
    project_has_news = sa.Table('project_has_news',sa.MetaData(), autoload_with=engine)

    open_call = sa.Table('open_call',sa.MetaData(), autoload_with=engine)
    project_has_open_call = sa.Table('project_has_open_call',sa.MetaData(), autoload_with=engine)

    organisation = sa.Table('organisation',sa.MetaData(), autoload_with=engine)
    project_has_organisation = sa.Table('project_has_organisation',sa.MetaData(), autoload_with=engine)

    project_review = sa.Table('project_review',sa.MetaData(), autoload_with=engine)    


    q = session.query(
        project
        ).filter(
            project.c.id == id
        ).first()




    aa = session.query(
        ai_asset.c.id
    ).join(
        project_has_ai_asset,project_has_ai_asset.c.project_id == id
    ).filter(
        ai_asset.c.id == project_has_ai_asset.c.ai_asset_id
    ).all()


    cs = session.query(
        case_study.c.id
    ).join(
        project_has_case_study,project_has_case_study.c.project_id == id
    ).filter(
        case_study.c.id == project_has_case_study.c.case_study_id
    ).all()


    er = session.query(
        educational_resource.c.id
    ).join(
        project_has_educational_resource,project_has_educational_resource.c.project_id == id
    ).filter(
        educational_resource.c.id == project_has_educational_resource.c.educational_resource_id
    ).all()

    n = session.query(
        news.c.id
    ).join(
        project_has_news,project_has_news.c.project_id == id
    ).filter(
        news.c.id == project_has_news.c.news_id
    ).all()

    ev = session.query(
        event.c.id
    ).join(
        project_has_event,project_has_event.c.project_id == id
    ).filter(
        event.c.id == project_has_event.c.event_id
    ).all()


    oc = session.query(
        open_call.c.id
    ).join(
        project_has_open_call,project_has_open_call.c.project_id == id
    ).filter(
        open_call.c.id == project_has_open_call.c.open_call_id
    ).all()

    
    org = session.query(
        organisation.c.id
    ).join(
        project_has_organisation,project_has_organisation.c.project_id == id
    ).filter(
        organisation.c.id == project_has_organisation.c.organisation_id
    ).all()


    r = session.query(
        project_review.c.comment
    ).filter(
        project_review.c.project_id == id
    ).all()
    
    ai_assets = []
    for x in aa:
        ai_assets.append(x[0])

    case_studies = []
    for x in cs:
        case_studies.append(x[0])

    educational_resources = []
    for x in er:
        educational_resources.append(x[0])

    events = []
    for x in ev:
        events.append(x[0])

    open_calls = []
    for x in oc:
        open_calls.append(x[0])

    organisations = []
    for x in org:
        organisations.append(x[0])

    reviews = []
    for x in r:
        reviews.append(x[0])


    
    result = {}
    result = dict(q)
    result["ai_assets"] = ai_assets
    result["case_studies"] = case_studies
    result["educational_resources"] = educational_resources
    result["events"] = events
    result["open_calls"] = open_calls
    result["organisations"] = organisations
    result["reviews"] = reviews

    
    return result


@app.get("/project/")
async def get_all_projects():

    project = sa.Table('project', sa.MetaData(), autoload_with=engine)

    q = session.query(
        project
        ).all()

    
    return q


@app.get("/research_bundle/{id}")
async def get_research_bundle(id):
    """
    id: ID for research_bundle that will be fetched
    """

    research_bundle = sa.Table('research_bundle', sa.MetaData(), autoload_with=engine)
    
    ai_asset = sa.Table('ai_asset',sa.MetaData(), autoload_with=engine)
    research_bundle_has_ai_asset = sa.Table('research_bundle_has_ai_asset',sa.MetaData(), autoload_with=engine)

    case_study = sa.Table('case_study',sa.MetaData(), autoload_with=engine)
    research_bundle_has_case_study = sa.Table('research_bundle_has_case_study',sa.MetaData(), autoload_with=engine)
    
    educational_resource = sa.Table('educational_resource',sa.MetaData(), autoload_with=engine)
    research_bundle_has_educational_resource = sa.Table('research_bundle_has_educational_resource',sa.MetaData(), autoload_with=engine)

    event = sa.Table('event',sa.MetaData(), autoload_with=engine)
    research_bundle_has_event = sa.Table('research_bundle_has_event',sa.MetaData(), autoload_with=engine)

    news = sa.Table('news',sa.MetaData(), autoload_with=engine)
    research_bundle_has_news = sa.Table('research_bundle_has_news',sa.MetaData(), autoload_with=engine)

    open_call = sa.Table('open_call',sa.MetaData(), autoload_with=engine)
    research_bundle_has_open_call = sa.Table('research_bundle_has_open_call',sa.MetaData(), autoload_with=engine)

    organisation = sa.Table('organisation',sa.MetaData(), autoload_with=engine)
    research_bundle_has_organisation = sa.Table('research_bundle_has_organisation',sa.MetaData(), autoload_with=engine)

    research_bundle_review = sa.Table('research_bundle_review',sa.MetaData(), autoload_with=engine)  

    tag = sa.Table('tag',sa.MetaData(), autoload_with=engine)  
    research_bundle_has_tag = sa.Table('research_bundle_has_tag',sa.MetaData(), autoload_with=engine)  

    technical_category = sa.Table('technical_category',sa.MetaData(), autoload_with=engine)
    research_bundle_has_technical_category = sa.Table('research_bundle_has_technical_category',sa.MetaData(), autoload_with=engine)  


    q = session.query(
        research_bundle
        ).filter(
            research_bundle.c.id == id
        ).first()




    aa = session.query(
        ai_asset.c.id
    ).join(
        research_bundle_has_ai_asset,research_bundle_has_ai_asset.c.research_bundle_id == id
    ).filter(
        ai_asset.c.id == research_bundle_has_ai_asset.c.ai_asset_id
    ).all()


    cs = session.query(
        case_study.c.id
    ).join(
        research_bundle_has_case_study,research_bundle_has_case_study.c.research_bundle_id == id
    ).filter(
        case_study.c.id == research_bundle_has_case_study.c.case_study_id
    ).all()


    er = session.query(
        educational_resource.c.id
    ).join(
        research_bundle_has_educational_resource,research_bundle_has_educational_resource.c.research_bundle_id == id
    ).filter(
        educational_resource.c.id == research_bundle_has_educational_resource.c.educational_resource_id
    ).all()

    n = session.query(
        news.c.id
    ).join(
        research_bundle_has_news,research_bundle_has_news.c.research_bundle_id == id
    ).filter(
        news.c.id == research_bundle_has_news.c.news_id
    ).all()

    ev = session.query(
        event.c.id
    ).join(
        research_bundle_has_event,research_bundle_has_event.c.research_bundle_id == id
    ).filter(
        event.c.id == research_bundle_has_event.c.event_id
    ).all()


    oc = session.query(
        open_call.c.id
    ).join(
        research_bundle_has_open_call,research_bundle_has_open_call.c.research_bundle_id == id
    ).filter(
        open_call.c.id == research_bundle_has_open_call.c.open_call_id
    ).all()

    
    org = session.query(
        organisation.c.id
    ).join(
        research_bundle_has_organisation,research_bundle_has_organisation.c.research_bundle_id == id
    ).filter(
        organisation.c.id == research_bundle_has_organisation.c.organisation_id
    ).all()


    t = session.query(
        tag.c.id
    ).join(
        research_bundle_has_tag,research_bundle_has_tag.c.research_bundle_id == id
    ).filter(
        tag.c.id == research_bundle_has_tag.c.tag_id
    ).all()

    t1 = session.query(
        technical_category.c.id
    ).join(
        research_bundle_has_technical_category,research_bundle_has_technical_category.c.research_bundle_id == id
    ).filter(
        technical_category.c.id == research_bundle_has_technical_category.c.technical_category_id
    ).all()


    r = session.query(
        research_bundle_review.c.comment
    ).filter(
        research_bundle_review.c.research_bundle_id == id
    ).all()
    
    ai_assets = []
    for x in aa:
        ai_assets.append(x[0])

    case_studies = []
    for x in cs:
        case_studies.append(x[0])

    educational_resources = []
    for x in er:
        educational_resources.append(x[0])

    events = []
    for x in ev:
        events.append(x[0])

    open_calls = []
    for x in oc:
        open_calls.append(x[0])

    organisations = []
    for x in org:
        organisations.append(x[0])

    reviews = []
    for x in r:
        reviews.append(x[0])

    tags = []
    for x in t:
        tags.append(x[0])

    technical_categories = []
    for x in t1:
        technical_categories.append(x[0])
    
    result = {}
    result = dict(q)
    result["ai_assets"] = ai_assets
    result["case_studies"] = case_studies
    result["educational_resources"] = educational_resources
    result["events"] = events
    result["open_calls"] = open_calls
    result["organisations"] = organisations
    result["reviews"] = reviews
    result["tags"] = tags
    result["technical_categories"] = technical_categories

    
    return result



@app.get("/research_bundle/")
async def get_all_research_bundles():

    research_bundle = sa.Table('research_bundle', sa.MetaData(), autoload_with=engine)

    q = session.query(
        research_bundle
        ).all()

    
    return q



@app.delete("/ai_asset/{id}")
async def delete_ai_asset(id):
    obj = Base.classes.ai_asset

    session.query(
        obj
        ).filter(
            obj.id == id
        ).delete()

    session.commit()

    return {"message": "OK"}


@app.delete("/organisation/{id}")
async def delete_organisation(id):
    obj = Base.classes.organisation

    session.query(
        obj
        ).filter(
            obj.id == id
        ).delete()

    session.commit()

    return {"message": "OK"}



@app.delete("/case_study/{id}")
async def delete_case_study(id):
    obj = Base.classes.case_study
    session.query(
        obj
        ).filter(
           obj.id == id
        ).delete()

    session.commit()

    return {"message": "OK"}



@app.delete("/educational_resource/{id}")
async def delete_educational_resource(id):
    obj = Base.classes.educational_resource
    session.query(
        obj
        ).filter(
           obj.id == id
        ).delete()

    session.commit()

    return {"message": "OK"}  


@app.delete("/event/{id}")
async def delete_event(id):
    obj = Base.classes.event
    session.query(
        obj
        ).filter(
           obj.id == id
        ).delete()

    session.commit()

    return {"message": "OK"}  

@app.delete("/news/{id}")
async def delete_news(id):
    obj = Base.classes.news
    session.query(
        obj
        ).filter(
           obj.id == id
        ).delete()

    session.commit()

    return {"message": "OK"}  


@app.delete("/open_call/{id}")
async def delete_open_call(id):
    obj = Base.classes.open_call
    session.query(
        obj
        ).filter(
           obj.id == id
        ).delete()

    session.commit()

    return {"message": "OK"}  


@app.delete("/project/{id}")
async def delete_open_call(id):
    obj = Base.classes.project
    session.query(
        obj
        ).filter(
           obj.id == id
        ).delete()

    session.commit()

    return {"message": "OK"}  


@app.delete("/research_bundle/{id}")
async def delete_open_call(id):
    obj = Base.classes.research_bundle
    session.query(
        obj
        ).filter(
           obj.id == id
        ).delete()

    session.commit()

    return {"message": "OK"}  