import os
from fastapi import FastAPI
from pydantic import BaseModel, Field
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Boolean, Date
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

database = Database(DATABASE_URL)
metadata = MetaData()

# items = Table(
#     "items",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String),
#     Column("description", String),
#     Column("price", Float),
#     Column("tax", Float),
# )

articles = Table(
    "articles",
    metadata,

    Column("articleId", Integer, primary_key=True),
    Column('authorId', Integer), # Integer
    Column('seriesId', Integer), # Integer
    Column('sections', String),
    Column('sectionLink', String),
    Column('sectionType', String),
    Column('articleTitle', String),
    Column('articleSubTitle', String),
    Column('isHidden', Boolean), # boolean maybe
    # Column('publishedDate', Date), # Need to fix this
    Column('numberOfFavorites', Integer), # Integer
    Column('series', Boolean), # boolean maybe
    Column('seriesChapter', Integer), # Integer
    Column('seriesType', String),
    Column('useVideoInsteadOfImage', Boolean), # boolean maybe
    Column('coverImageOrVideo', String),
    Column('article', String),
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

# class Item(BaseModel):
#     name: str
#     description: str = None
#     price: float
#     tax: float = None

class Article(BaseModel):
    articleId: int
    authorId: int
    seriesId: int
    sections: str
    sectionLink: str
    articleTitle: str
    articleSubTitle: str
    isHidden: bool
    # publishedDate: str = Field(alias="publishedDate") # Need to fix this
    numberOfFavorites: int
    series: bool
    seriesChapter: int
    seriesType: str
    useVideoInsteadOfImage: bool
    coverImageOrVideo: str
    article: str



# @app.post("/items/")
# async def create_item(item: Item):
#     query = items.insert().values(
#         name=item.name,
#         description=item.description,
#         price=item.price,
#         tax=item.tax,
#     )
#     await database.execute(query)
#     return item

@app.get("/articles/", response_model=list[Article])
async def get_articles():
    query = articles.select()
    return await database.fetch_all(query)

@app.middleware("http")
async def db_session_middleware(request, call_next):
    if not database.is_connected:
        await database.connect()
    response = await call_next(request)
    if database.is_connected:
        await database.disconnect()
    return response
