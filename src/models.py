import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

import enum
from sqlalchemy import String, Table, Column, Integer, MetaData, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base, str_256
from .crud_db import intpk, created_at, updated_at


class WorkersOrm(Base):
    __tablename__ = "workers"

    id: Mapped[intpk]
    username: Mapped[str_256]
    resumes: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="workers",
    )
    resumes_parttime: Mapped[list["ResumesOrm"]] = relationship(
        back_populates="workers",
        primaryjoin='and_(WorkersOrm.id == ResumesOrm.worker_id, ResumesOrm.workload == "parttime")',
        order_by="ResumesOrm.id.desc()",
        lazy="selectin",
    )


class Workload(enum.Enum):
    parttime = "parttime"
    fulltime = "fulltime"


class ResumesOrm(Base):
    __tablename__ = "resumes"

    id: Mapped[intpk]
    title: Mapped[str_256]
    salary: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    workers: Mapped["WorkersOrm"] = relationship(
        back_populates="resumes",
    )

    repr_cols_num = 3
    # repr_cols = ('created_at')


metadata_obj = MetaData()


workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)
