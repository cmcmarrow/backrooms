"""
Copyright 2021 Charles McMarrow

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Hold test files.
"""

# built-in
import os


def get_path(file_name: str) -> str:
    """
    info: Gets the absolute path to test file.
    :param file_name: str
    :return: str
    """
    return os.path.join(os.path.dirname(__file__), file_name)
