import requests
import datetime as dt

from models import Setting
from version import APP_VERSION
from repositories.settings_repository import SettingsRepository

class VersionService:

    def __init__(self, settings_repo: SettingsRepository):

        self.GITHUB_API = (
            "https://api.github.com/repos/Splatbeef/LMUStrategyTool/releases/latest"
        )
        self.repo = settings_repo

    def get_latest_version(self) -> str | None:
        try:
            # last_check = self.repo.get_by_key("VersionCheck")
            # if last_check.value_str == str(dt.date.today()):
            #     return APP_VERSION
            response = requests.get(
                self.GITHUB_API,
                timeout=5
            )
            print("Got Response")

            response.raise_for_status()

            return response.json()["tag_name"].lstrip("v")

        except Exception:
            return "Check Failed"

    def check_version(self) -> dict:

        latest = self.get_latest_version()

        dct = {"current": APP_VERSION}
        if latest == "Check Failed":
            dct["status"]="Check Failed"
        else:
            dct["latest"]=latest
            dct["status"]="Success"
            dct["up_to_date"]= latest==APP_VERSION

        return dct

    def update_version(self, previous: Setting):

        #transfer logic here if needed

        self.repo.update(
            Setting(
                id=previous.id,
                key="Version",
                value_str = APP_VERSION,
                value_bool = None,
                value_int = None,
                value_float = None
            )
        )