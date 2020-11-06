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

from manager.logger import initLogger
from manager.configuration import conf, storage_path
from manager import storage
from manager import export
from manager import api
import falcon


initLogger(conf.Logger.level)

storage_handler = storage.Handler(storage_path)

export_handler = export.Handler(
    (
        "{}/{}".format(conf.MachineRegistry.url, conf.MachineRegistry.api),
        "{}/{}".format(conf.WorkerRegistry.url, conf.WorkerRegistry.api),
        "{}/{}".format(conf.ProtocolAdapterRegistry.url, conf.ProtocolAdapterRegistry.api),
        "{}/{}".format(conf.PipelineRegistry.url, conf.PipelineRegistry.api)
    ),
    storage_handler,
    conf.Backup.max_days
)

if conf.Backup.automatic:
    export_handler.start()

app = falcon.API()

app.req_options.strip_url_path_trailing_slash = True

routes = (
    ("/backups", api.Backups(export_handler, storage_handler)),
    ("/backups/{backup}", api.Backup(export_handler, storage_handler))
)

for route in routes:
    app.add_route(*route)
