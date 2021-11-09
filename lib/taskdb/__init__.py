from .HomeworkAll import AllTasks
from .HomeworkArchive import ArchiveTasks
from .HomeworkCurrent import CurrentTasks
from .HomeworkDetailed import DetailedInfo
from .HomeworkRecord import InsertHW
from .HomeworkDBgen import createDB
from .HomeworkSubjects import SubjectList
from .HomeworkUpdate import UpdateHW, SetArchiveHW
from .HomeworkDelete import DeleteHW

def checkDB(db):
    import os.path

    if os.path.isfile(db):
        pass
    else:
        createDB(db)