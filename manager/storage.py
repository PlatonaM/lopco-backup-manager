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


__all__ = ("Handler", )


import typing
import os
import io


class Handler(object):
    def __init__(self, path, chunk_size_bytes=4096):
        self.__storage_path = path
        self.__chunk_size_bytes = chunk_size_bytes

    def write(self, stream: io.BytesIO, f_name: str):
        with open(os.path.join(self.__storage_path, f_name), 'wb') as file:
            while True:
                chunk = stream.read(self.__chunk_size_bytes)
                if not chunk:
                    break
                file.write(chunk)

    def read(self, f_name: str) -> typing.Tuple[typing.BinaryIO, int]:
        file_path = os.path.join(self.__storage_path, f_name)
        stream = open(file_path, 'rb')
        size = os.path.getsize(file_path)
        return stream, size

    def list(self) -> typing.List[typing.Tuple[str, int]]:
        files = list()
        for file in os.listdir(self.__storage_path):
            files.append((file, os.path.getsize(os.path.join(self.__storage_path, file))))
        return files

    def delete(self, f_name: str):
        os.remove(os.path.join(self.__storage_path, f_name))
