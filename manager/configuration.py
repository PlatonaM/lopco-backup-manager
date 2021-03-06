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

__all__ = ("conf", "storage_path")


import simple_env_var


@simple_env_var.configuration
class Conf:

    @simple_env_var.section
    class Backup:
        endpoints = "http://pipeline-registry/pipelines;http://machine-registry/machines;http://worker-registry/workers;http://protocol-adapter-registry/protocol-adapters"
        delimiter = ";"

    @simple_env_var.section
    class AutoBackup:
        enabled = True
        max_days = 60
        interval = 10800
        hour = 1
        minute = 30
        second = 0

    @simple_env_var.section
    class Logger:
        level = "info"


conf = Conf(load=False)

storage_path = "/backups"
