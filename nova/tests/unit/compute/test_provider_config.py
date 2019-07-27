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

import fixtures
from jsonschema.exceptions import ValidationError
from oslotest import base
import pkg_resources
import uuid

from nova.compute import provider_config


class LoadingTestCases(base.BaseTestCase):
    def test_loading(self):
        path = pkg_resources.resource_filename(
            __name__, 'provider_config_data/example_provider.yaml')
        data = provider_config.parse_provider_yaml(path)
        self.assertEqual(
            {'meta':
                {'schema_version': '1.0'},
             'providers':
                 [{'identification': {'name': 'foo'}}]
             },
            data)

    def test_loading_fail(self):
        path = pkg_resources.resource_filename(
            __name__, 'provider_config_data/invalid_path/!@#.yaml')
        self.assertRaises(IOError,
                          provider_config.parse_provider_yaml, path)


class SchemaValidationTestCases(base.BaseTestCase):
    def setUp(self):
        super(SchemaValidationTestCases, self).setUp()
        self.mock_load_yaml = self.useFixture(
            fixtures.MockPatchObject(
                provider_config, '_load_yaml_file')).mock
        self.mock_uuid = str(uuid.uuid4())

    def test_no_metadata(self):
        reference = {'providers': [
                        {'identification': {'uuid': self.mock_uuid}}]}
        self.mock_load_yaml.return_value = reference

        self.assertRaises(ValidationError,
                          provider_config.parse_provider_yaml, None)

    def test_no_schema_version(self):
        reference = {'meta': {},
                     'providers': [
                         {'identification': {'uuid': 'invalid!@#'}}]}
        self.mock_load_yaml.return_value = reference

        self.assertRaises(ValidationError,
                          provider_config.parse_provider_yaml, None)

    def test_invalid_schema_version(self):
        reference = {'meta': {'schema_version': '!@#'},
                     'providers': [
                         {'identification': {'uuid': 'invalid!@#'}}]}
        self.mock_load_yaml.return_value = reference

        self.assertRaises(ValidationError,
                          provider_config.parse_provider_yaml, None)

    def test_provider_by_uuid(self):
        reference = {'meta': {'schema_version': '1.0'},
                     'providers': [
                         {'identification': {'uuid': self.mock_uuid}}]}
        self.mock_load_yaml.return_value = reference

        actual = provider_config.parse_provider_yaml(None)

        self.assertEqual(reference, actual)

    def test_provider_invalid_uuid(self):
        reference = {'meta': {'schema_version': '1.0'},
                     'providers': [
                         {'identification': {'uuid': 'not-quite-a-uuid'}}]}
        self.mock_load_yaml.return_value = reference

        self.assertRaises(ValidationError,
                          provider_config.parse_provider_yaml, None)

    def test_provider_by_name(self):
        reference = {'meta': {'schema_version': '1.0'},
                     'providers': [
                         {'identification': {'name': 'custom_provider'}}]}
        self.mock_load_yaml.return_value = reference

        actual = provider_config.parse_provider_yaml(None)

        self.assertEqual(reference, actual)

    def test_provider_null_name(self):
        reference = {'meta': {'schema_version': '1.0'},
                     'providers': [
                         {'identification': {'name': ''}}]}
        self.mock_load_yaml.return_value = reference

        self.assertRaises(ValidationError,
                          provider_config.parse_provider_yaml, None)

    def test_provider_uuid_and_name(self):
        pass

    def test_provider_no_identification(self):
        reference = {'meta': {'schema_version': '1.0'},
                     'providers': [
                         {'inventories': ['123']}]}
        self.mock_load_yaml.return_value = reference

        self.assertRaises(ValidationError,
                          provider_config.parse_provider_yaml, None)

    def test_inventories_invalid_adjective(self):
        pass

    def test_inventories_one_additional_resource_class(self):
        pass

    def test_inventories_one_additional_resource_class_no_total(self):
        pass

    def test_inventories_one_additional_resource_class_invalid_total(self):
        pass

    def test_inventories_one_additional_resource_class_additional_property(self):
        pass

    def test_inventories_multiple_additional_resource_classes(self):
        pass

    def test_inventories_multiple_additional_resource_classes_one_invalid(self):
        pass

    def test_traits_invalid_adjective(self):
        pass

    def test_traits_one_additional_trait(self):
        pass

    def test_traits_one_additional_trait_invalid(self):
        pass

    def test_traits_multiple_additional_traits(self):
        pass

    def test_traits_multiple_additional_traits_one_invalid(self):
        pass
