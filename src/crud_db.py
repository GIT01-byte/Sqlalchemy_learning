import datetime
from typing import Annotated
from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy_utc import UtcDateTime, utcnow

import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(UtcDateTime(), server_default=utcnow(), nullable=False)]
updated_at = Annotated[datetime.datetime, mapped_column(DateTime(timezone=True), server_default=utcnow(), onupdate=utcnow(), nullable=False)]
