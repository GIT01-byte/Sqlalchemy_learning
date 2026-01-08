import time
from models import Workload
from queries.core import SyncCore
from queries.orm import SyncOrm


# SyncCore.create_tables()


# SyncCore.insert_workers()
# SyncCore.select_workers()


# SyncCore.update_workers()
# SyncCore.select_workers()

SyncOrm.create_tables()


SyncOrm.insert_workers(username='Jack')
SyncOrm.insert_workers(username='Ivan')

SyncOrm.insert_resumes(title="Software Engineer (Python)", salary=125000, workload=Workload.fulltime, worker_id=1)
SyncOrm.insert_resumes(title="Data Scientist (Python)", salary=135000, workload=Workload.fulltime, worker_id=2)
SyncOrm.insert_resumes(title="Web Developer (JavaScript)", salary=120000, workload=Workload.parttime, worker_id=1)
SyncOrm.insert_resumes(title="Frontend Developer (C++)", salary=98000, workload=Workload.fulltime, worker_id=2)
SyncOrm.insert_resumes(title="Backend Developer (C#)", salary=110000, workload=Workload.fulltime, worker_id=1)
SyncOrm.insert_resumes(title="Mobile App Developer (Go)", salary=40000, workload=Workload.parttime, worker_id=2)
SyncOrm.insert_resumes(title="DevOps Engineer (Ruby)", salary=140000, workload=Workload.fulltime, worker_id=1)
SyncOrm.insert_resumes(title="Data Analyst (C++)", salary=85000, workload=Workload.fulltime, worker_id=2)
SyncOrm.insert_resumes(title="Machine Learning Engineer (Python)", salary=150000, workload=Workload.fulltime, worker_id=1)
SyncOrm.insert_resumes(title="Cloud Engineer (PHP)", salary=130000, workload=Workload.fulltime, worker_id=2)
SyncOrm.insert_resumes(title="Security Engineer (Python)", salary=75000, workload=Workload.parttime, worker_id=1)
SyncOrm.insert_resumes(title="Project Manager (Rust)", salary=105000, workload=Workload.fulltime, worker_id=2)
SyncOrm.insert_resumes(title="Product Manager (SQL)", salary=115000, workload=Workload.fulltime, worker_id=1)
SyncOrm.insert_resumes(title="UX Designer (HTML)", salary=10000, workload=Workload.parttime, worker_id=2)
SyncOrm.insert_resumes(title="UI Designer (CSS)", salary=92000, workload=Workload.fulltime, worker_id=1)

SyncOrm.select_workers()
SyncOrm.select_resumes()

SyncOrm.update_resumes(resume_id=5, new_title='Data Scientist (Python)', new_workload=Workload.fulltime)
SyncOrm.update_workers(worker_id=1, new_username='Timur')

SyncOrm.select_workers()
SyncOrm.select_resumes()

SyncOrm.select_resumes_avg_salary('Python')
SyncOrm.join_cte_subquery_window_func('Python')

# SyncOrm.select_workers_lazy_realtionship()
# SyncOrm.select_workers_joined_realtionship()
SyncOrm.select_workers_selectinload_realtionship()
SyncOrm.select_workers_codition_realtionship_contains_eager()
SyncOrm.select_workers_codition_realtionship_contains_eager_limit()
