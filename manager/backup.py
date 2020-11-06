"""
   Copyright 2020 InfAI (CC SES)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


__all__ = ("Handler",)


from .logger import getLogger
from .util import getDelay
from . import storage
from . import model
import threading
import datetime
import requests
import time
import json
import io


logger = getLogger(__name__.split(".", 1)[-1])


class BackupError(Exception):
    pass


class CreateExportError(BackupError):
    pass


class AddBackupError(BackupError):
    pass


class GetBackupError(BackupError):
    pass


class DeleteBackupError(BackupError):
    pass


class ListBackupsError(BackupError):
    pass


class Handler(threading.Thread):
    __exp_prefix = "export-"
    __imp_prefix = "import-"
    __extension = "json"

    def __init__(self, endpoints: tuple, storage_handler: storage.Handler, max_age: int):
        super().__init__(name="backup-worker", daemon=True)
        self.__endpoints = endpoints
        self.__st_handler = storage_handler
        self.__max_age = max_age

    def __getData(self) -> dict:
        data = dict()
        for endpoint in self.__endpoints:
            resp = requests.get(url=endpoint)
            if not resp.ok:
                raise RuntimeError("could not get data from '{}' - {}".format(endpoint, resp.status_code))
            data[endpoint] = dict()
            for key, value in resp.json().items():
                data[endpoint][key] = json.loads(value)
        return data

    def __removeOldExports(self):
        files = self.__st_handler.list()
        for file in files:
            if self.__exp_prefix in file[0]:
                timestamp = file[0].rsplit(".", 1)[0]
                age = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") + datetime.timedelta(days=self.__max_age)
                if age < datetime.datetime.utcnow():
                    self.__st_handler.delete(file[0])

    def create(self):
        try:
            self.__st_handler.write(
                io.BytesIO(json.dumps(self.__getData()).encode()),
                "{}{}Z.{}".format(self.__exp_prefix, datetime.datetime.utcnow().isoformat(), self.__extension)
            )
        except Exception as ex:
            raise CreateExportError("creating export failed - {}".format(ex))

    def add(self, stream: io.BytesIO):
        try:
            return self.__st_handler.write(
                stream,
                "{}{}Z.{}".format(self.__imp_prefix, datetime.datetime.utcnow().isoformat(), self.__extension)
            )
        except Exception as ex:
            raise AddBackupError("adding backup failed - {}".format(ex))

    def get(self, backup: str):
        try:
            f_name = "{}.{}".format(backup, self.__extension)
            stream, size = self.__st_handler.read(f_name)
            return stream, size, f_name
        except FileNotFoundError:
            raise
        except Exception as ex:
            raise GetBackupError("retrieving backup failed - {}".format(ex))

    def delete(self, backup: str):
        try:
            self.__st_handler.delete("{}.{}".format(backup, self.__extension))
        except FileNotFoundError:
            raise
        except Exception as ex:
            raise DeleteBackupError("removing backup failed - {}".format(ex))

    def list(self) -> list:
        try:
            files = self.__st_handler.list()
            backups = list()
            for file, size in files:
                name = file.rsplit(".", 1)[0]
                backups.append(
                    {
                        model.Backup.name: name,
                        model.Backup.time: name.split("-", 1)[-1],
                        model.Backup.file: file,
                        model.Backup.size: size
                    }
                )
            if backups:
                backups.sort(key=lambda item: item[model.Backup.time], reverse=True)
            return backups
        except Exception as ex:
            raise ListBackupsError("listing backups failed - {}".format(ex))

    def run(self) -> None:
        logger.info("automatic backup enabled")
        while True:
            try:
                time.sleep(getDelay())
                logger.info("starting automatic backup ...")
                self.create()
            except Exception as ex:
                logger.error("automatic backup failed - {}".format(ex))
            try:
                logger.info("removing exports older than '{}' days ...".format(self.__max_age))
                self.__removeOldExports()
            except Exception as ex:
                logger.error("removing old exports failed - {}".format(ex))
