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


from . import model
from . import storage
from .logger import getLogger
from .util import getDelay
import threading
import datetime
import requests
import typing
import time
import json
import io


logger = getLogger(__name__.split(".", 1)[-1])


class ExportError(Exception):
    pass


class CreateExportError(ExportError):
    pass


class GetExportError(ExportError):
    pass


class ListExportsError(ExportError):
    pass


class RemoveExportError(ExportError):
    pass


class Handler(threading.Thread):
    def __init__(self, endpoints: tuple, storage_handler: storage.Handler):
        super().__init__(name="backup-worker", daemon=True)
        self.__endpoints = endpoints
        self.__st_handler = storage_handler

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

    def createExport(self):
        try:
            self.__st_handler.write(
                io.BytesIO(json.dumps(self.__getData()).encode()),
                "{}Z".format(datetime.datetime.utcnow().isoformat())
            )
        except Exception as ex:
            raise CreateExportError("creating export failed - {}".format(ex))

    def getExport(self, name: str):
        try:
            return self.__st_handler.read(name)
        except FileNotFoundError:
            raise
        except Exception as ex:
            raise GetExportError("retrieving export '{}' failed - {}".format(name, ex))

    def listExports(self) -> typing.List[dict]:
        try:
            files = self.__st_handler.list()
            exports = list()
            for file, size in files:
                exports.append(
                    {
                        model.Export.file: file,
                        model.Export.time: file.rsplit(".", 1)[0],
                        model.Export.size: size
                    }
                )
            if exports:
                exports.sort(key=lambda item: item[model.Export.time], reverse=True)
            return exports
        except Exception as ex:
            raise ListExportsError("listing exports failed - {}".format(ex))

    def removeExport(self, name: str):
        try:
            return self.__st_handler.delete(name)
        except FileNotFoundError:
            raise
        except Exception as ex:
            raise RemoveExportError("removing export '{}' failed - {}".format(name, ex))

    def run(self) -> None:
        logger.info("automatic export enabled")
        while True:
            try:
                time.sleep(getDelay())
                logger.info("starting automatic export ...")
                self.createExport()
            except Exception as ex:
                logger.error("automatic export failed - {}".format(ex))
