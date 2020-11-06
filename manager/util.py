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


from .configuration import conf
import datetime
import hashlib


__all__ = ("getDelay", "genHash")


def getDelay():
    x = datetime.datetime.today()
    if not any((conf.AutoBackup.hour, conf.AutoBackup.minute, conf.AutoBackup.second)):
        y = x.replace(day=x.day, hour=x.hour, minute=x.minute, second=x.second, microsecond=0) + datetime.timedelta(seconds=conf.AutoBackup.interval)
        delay = y - x
        return delay.total_seconds()
    if conf.AutoBackup.second and not conf.AutoBackup.minute and not conf.AutoBackup.hour:
        y = x.replace(day=x.day, hour=x.hour, minute=x.minute, second=conf.AutoBackup.second, microsecond=0)
        delta = datetime.timedelta(minutes=1)
    if conf.AutoBackup.minute and not conf.AutoBackup.second and not conf.AutoBackup.hour:
        y = x.replace(day=x.day, hour=x.hour, minute=conf.AutoBackup.minute, second=0, microsecond=0)
        delta = datetime.timedelta(hours=1)
    if conf.AutoBackup.minute and conf.AutoBackup.second and not conf.AutoBackup.hour:
        y = x.replace(day=x.day, hour=x.hour, minute=conf.AutoBackup.minute, second=conf.AutoBackup.second, microsecond=0)
        delta = datetime.timedelta(hours=1)
    if conf.AutoBackup.hour and not conf.AutoBackup.minute and not conf.AutoBackup.second:
        y = x.replace(day=x.day, hour=conf.AutoBackup.hour, minute=0, second=0, microsecond=0)
        delta = datetime.timedelta(days=1)
    if conf.AutoBackup.hour and any((conf.AutoBackup.minute, conf.AutoBackup.second)):
        y = x.replace(day=x.day, hour=conf.AutoBackup.hour, minute=conf.AutoBackup.minute or 0, second=conf.AutoBackup.second or 0, microsecond=0)
        delta = datetime.timedelta(days=1)
    delay = y - x
    if delay.total_seconds() <= 0:
        y = y + delta
        delay = y - x
    return delay.total_seconds()
