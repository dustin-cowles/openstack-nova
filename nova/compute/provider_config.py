#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import jsonschema
import pkg_resources
import yaml

from oslo_utils import uuidutils

# This entire file is very generic, perhaps this can be made reusable

# TODO(dustinc): Load from config
_SCHEMA_FILE = 'provider_config_schema.yaml'
_SCHEMA_DICT = None


@jsonschema.FormatChecker.cls_checks('uuid')
def _validate_uuid_format(instance):
    return uuidutils.is_uuid_like(instance)


def _load_schema():
    global _SCHEMA_DICT
    if _SCHEMA_DICT is None:
        with pkg_resources.resource_stream(__name__, _SCHEMA_FILE) as f:
            _SCHEMA_DICT = yaml.safe_load(f)
    return _SCHEMA_DICT


def _load_yaml_file(path):
    with open(path) as f:
        return yaml.safe_load(f)


def parse_provider_yaml(path):
    """Loads, validates, and parses a provider.yaml file into a dict.

    :param path: File system path to the file to parse.
    :return: dict representing the contents of the file.
    :raise: jsonschema.exceptions.ValidationError if the specified file does
            not validate against the schema.
    """
    yaml_file = _load_yaml_file(path)
    jsonschema.validate(yaml_file, _load_schema())
    return yaml_file
