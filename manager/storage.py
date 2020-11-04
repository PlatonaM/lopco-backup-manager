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


__all__ = ("Handler", "StorageError", "WriteError", "ReadError", "ListError", "DeleteError")


import typing
import os
import io


class StorageError(Exception):
    pass


class WriteError(StorageError):
    pass


class ReadError(StorageError):
    pass


class ListError(StorageError):
    pass


class DeleteError(StorageError):
    pass


class Handler(object):
    def __init__(self, path, extension, chunk_size_bytes=4096):
        self.__storage_path = path
        self.__extension = extension
        self.__chunk_size_bytes = chunk_size_bytes

    def write(self, stream: io.BytesIO, name: str):
        try:
            with open(os.path.join(self.__storage_path, "{}.{}".format(name, self.__extension)), 'wb') as file:
                while True:
                    chunk = stream.read(self.__chunk_size_bytes)
                    if not chunk:
                        break
                    file.write(chunk)
        except Exception as ex:
            raise WriteError("writing '{}' failed - {}".format("{}.{}".format(name, self.__extension), ex))

    def read(self, name: str) -> typing.Tuple[typing.BinaryIO, int]:
        try:
            file_path = os.path.join(self.__storage_path, "{}.{}".format(name, self.__extension))
            stream = open(file_path, 'rb')
            size = os.path.getsize(file_path)
            return stream, size
        except FileNotFoundError:
            raise FileNotFoundError("file '{}' does not exist".format("{}.{}".format(name, self.__extension)))
        except Exception as ex:
            raise ReadError("reading '{}' failed - {}".format("{}.{}".format(name, self.__extension), ex))

    def list(self):
        try:
            return os.listdir(self.__storage_path)
        except Exception as ex:
            raise ListError("listing files failed - {}".format(ex))

    def delete(self, name: str):
        try:
            os.remove(os.path.join(self.__storage_path, "{}.{}".format(name, self.__extension)))
        except Exception as ex:
            raise DeleteError("deleting '{}' failed - {}".format("{}.{}".format(name, self.__extension), ex))
