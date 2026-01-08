from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, mapped_column

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
)


sync_session_factory= sessionmaker(sync_engine)

str_256 = Annotated[str, mapped_column(String(256))]
class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')
        
        return f'<{self.__class__.__name__} {', '.join(cols)}>'
