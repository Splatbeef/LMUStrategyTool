import datetime as dt
import pandas as pd

from models import *
from Repositories.carclass_repository import *
from services import *


db = DatabaseService()

repo = CarClassRepository(db)

classes=["Hypercar", "LMP2 (ELMS)", "LMP2 (WEC)", "LMP3", "LMGT3", "LMGTE"]

for c in classes:
    if not repo.exists(c):
        print(f"Adding {c}")
        repo.add(
            CarClass(
                id=None,
                name=c
            )
        )

print(repo.get_all())