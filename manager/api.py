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

__all__ = ("Backups", "Backup")


from .logger import getLogger
from . import backup
from . import storage
from . import model
import falcon
import json


logger = getLogger(__name__.split(".", 1)[-1])


def reqDebugLog(req):
    logger.debug("method='{}' path='{}' content_type='{}'".format(req.method, req.path, req.content_type))

def reqErrorLog(req, ex):
    logger.error("method='{}' path='{}' - {}".format(req.method, req.path, ex))


class Backups:
    def __init__(self, bk_handler: backup.Handler):
        self.__bk_handler = bk_handler

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        try:
            resp.body = json.dumps(self.__bk_handler.list())
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_patch(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        try:
            self.__bk_handler.create()
            resp.status = falcon.HTTP_200
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_post(self, req: falcon.request.Request, resp: falcon.response.Response):
        reqDebugLog(req)
        try:
            self.__bk_handler.add(req.stream)
            resp.status = falcon.HTTP_200
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)


class Backup:
    def __init__(self, bk_handler: backup.Handler):
        self.__bk_handler = bk_handler

    def on_get(self, req: falcon.request.Request, resp: falcon.response.Response, backup):
        reqDebugLog(req)
        try:
            resp.stream, resp.content_length, f_name = self.__bk_handler.get(backup)
            resp.downloadable_as = f_name
            resp.content_type = falcon.MEDIA_JSON
            resp.status = falcon.HTTP_200
        except FileNotFoundError as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_patch(self, req: falcon.request.Request, resp: falcon.response.Response, backup):
        reqDebugLog(req)
        try:
            self.__bk_handler.apply(backup)
            resp.status = falcon.HTTP_200
        except FileNotFoundError as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)

    def on_delete(self, req: falcon.request.Request, resp: falcon.response.Response, backup):
        reqDebugLog(req)
        try:
            self.__bk_handler.delete(backup)
            resp.status = falcon.HTTP_200
        except FileNotFoundError as ex:
            resp.status = falcon.HTTP_404
            reqErrorLog(req, ex)
        except Exception as ex:
            resp.status = falcon.HTTP_500
            reqErrorLog(req, ex)
