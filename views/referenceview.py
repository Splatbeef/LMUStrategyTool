import flet as ft

from models import Car, Track, ReferenceTime
from Repositories.referencetime_repository import * 
from services.referenceservice import *

class ReferenceView(ft.Container):
    def __init__(self, reference_repo, track_repo):
        pass

    def sync_clicked(self, e):
        pass