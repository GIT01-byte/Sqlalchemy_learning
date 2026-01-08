
from sqlalchemy import insert, select, text, update
from database import Base, sync_engine, async_engine, sync_session_factory
from models import WorkersOrm, workers_table


class SyncCore:
    @staticmethod
    def create_tables():
        sync_engine.echo=False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo=True

    @staticmethod
    def insert_workers():
        with sync_session_factory() as conn:
            stmt = insert(WorkersOrm).values(
                [
                    {'username': 'Debug'},
                    {'username': 'Debug1'},
                ]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_session_factory() as conn:
            query = select(workers_table)
            result = conn.execute(query)
            print(f'{result.all()=}')

    @staticmethod
    def update_workers(worker_id: int = 2, new_username: str = 'Debug2'):
        with sync_session_factory() as conn:
            # stmt = text('UPDATE workers SET username=:new_username WHERE id=:id')
            # stmt = stmt.bindparams(new_username=new_username, id=worker_id)
            stmt = update(workers_table).values(username=new_username).filter_by(id=worker_id)
            conn.execute(stmt)
            conn.commit()

class AsyncCore:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            async_engine.echo = False
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            async_engine.echo = True
