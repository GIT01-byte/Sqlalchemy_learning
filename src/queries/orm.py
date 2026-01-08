
from sqlalchemy import Integer, and_, func, select
from sqlalchemy.orm import aliased, joinedload, selectinload, contains_eager
from database import Base, sync_engine, sync_session_factory
from models import ResumesOrm, WorkersOrm, Workload


class SyncOrm:
    @staticmethod
    def create_tables():
        sync_engine.echo=False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo=True

    
    @staticmethod
    def insert_workers(username: str):
        with sync_session_factory() as session:
            worker = WorkersOrm(username=username)
            session.add(worker)
            session.commit()
            session.refresh(worker)

    @staticmethod
    def select_workers():
        with sync_session_factory() as session:
            query = select(WorkersOrm)
            result = session.execute(query)
            print(f'{result.scalars().all()=}')

    @staticmethod
    def update_workers(worker_id: int, new_username: str | None = None):
        with sync_session_factory() as session:
            worker = session.get(WorkersOrm, worker_id)
            if worker:
                if new_username is not None:
                    worker.username = new_username
                session.commit()
                session.refresh(worker)
            else:
                raise ValueError(f'Работник, имеющий id: {worker_id} не найден')

    @staticmethod
    def insert_resumes(title: str, salary: int | None = None, workload: Workload | None = None, worker_id: int | None = None):
        with sync_session_factory() as session:
            resume = ResumesOrm(title=title, salary=salary, workload=workload, worker_id=worker_id)
            session.add(resume)
            session.commit()
            session.refresh(resume)

    @staticmethod
    def select_resumes():
        with sync_session_factory() as session:
            query = select(ResumesOrm)
            result = session.execute(query)
            print(f'{result.scalars().all()=}')

    @staticmethod
    def update_resumes(resume_id: int, new_title: str | None = None, new_salary: str | None = None, new_workload: Workload | None = None):
        with sync_session_factory() as session:
            resume = session.get(ResumesOrm, resume_id)
            if resume:
                if new_title is not None:
                    resume.title = new_title
                if new_salary is not None:
                    resume.salary = new_salary
                if new_workload is not None:
                    resume.workload = new_workload
                session.commit()
                session.refresh(resume)
            else:
                raise ValueError(f"Резюме, имеющее id: {resume_id} не надйено")

    @staticmethod
    def select_resumes_avg_salary(like_language: str):
        with sync_session_factory() as session:
            query = (
                select(ResumesOrm)
                .select_from(ResumesOrm)
                .filter(and_(
                ResumesOrm.title.contains(like_language),
                ResumesOrm.salary > 40000))
                )
            print(query.compile(compile_kwargs={'literal_binds': True}))
            result = session.execute(query)
            print(f'{result.scalars().all()=}')

    @staticmethod
    def join_cte_subquery_window_func(like_language: str):
        with sync_session_factory() as session:
            """
            WITH process_2 AS(
            SELECT *, salary-avg_workload_salary AS salary_diff
            FROM
            (SELECT
                w.id,
                w.username,
                r.salary,
                r.workload,
                avg(r.salary) OVER(PARTITION BY workload)::int AS avg_workload_salary
            FROM resumes r
            JOIN workers w ON r.worker_id = w.id) process_1)

            SELECT * FROM process_2
            ORDER BY salary_diff DESC
            """
            r = aliased(ResumesOrm)
            w = aliased(WorkersOrm)
            subq = (
                select(
                    r,
                    w,
                    func.avg(r.salary).over(partition_by=r.workload).cast(Integer).label('avg_workload_salary'),
                )
                .join(r, r.worker_id == w.id).subquery('process_1')
            )
            cte = (
                select(
                    subq.c.worker_id,
                    subq.c.username,
                    subq.c.salary,
                    subq.c.workload,
                    subq.c.avg_workload_salary,
                    (subq.c.salary-subq.c.avg_workload_salary).label('salary_diff'),
                )
                .cte('process_2')
            )
            query = (
                select(cte)
                .order_by(cte.c.salary_diff.desc())
            )
            print(query.compile(compile_kwargs={'literal_binds': True}))
            result = session.execute(query)
            print(f'{result.all()=}')

    @staticmethod
    def select_workers_lazy_realtionship():
        with sync_session_factory() as session:
            query = (
                select(WorkersOrm)
                )
            res = session.execute(query)
            result = res.scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)

    @staticmethod
    def select_workers_joined_realtionship():
        with sync_session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(joinedload(WorkersOrm.resumes))
                )
            res = session.execute(query)
            result = res.unique().scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)

    @staticmethod
    def select_workers_selectinload_realtionship():
        with sync_session_factory() as session:
            query = (
                select(WorkersOrm)
                .options(selectinload(WorkersOrm.resumes))
                )
            res = session.execute(query)
            result = res.unique().scalars().all()

            worker_1_resumes = result[0].resumes
            print(worker_1_resumes)

            worker_2_resumes = result[1].resumes
            print(worker_2_resumes)

    @staticmethod
    def select_workers_codition_realtionship_contains_eager():
        with sync_session_factory() as session:
            query = (
                select(WorkersOrm)
                .join(WorkersOrm.resumes)
                .options(contains_eager(WorkersOrm.resumes))
                .filter(ResumesOrm.workload == 'parttime')
                )
            result = session.execute(query)
            print(f'{result.unique().scalars().all()=}')

    @staticmethod
    def select_workers_codition_realtionship_contains_eager_limit():
        with sync_session_factory() as session:
            subq = (
                select(ResumesOrm.id.label('parttime_resume_id'))
                .filter(ResumesOrm.worker_id == WorkersOrm.id)
                .order_by(WorkersOrm.id.desc())
                .limit(1)
                .scalar_subquery()
                .correlate(WorkersOrm)
            )
            query = (
                select(WorkersOrm)
                .join(ResumesOrm, ResumesOrm.id.in_(subq))
                .options(contains_eager(WorkersOrm.resumes))
                )
            result = session.execute(query)
            print(f'{result.unique().scalars().all()=}')


