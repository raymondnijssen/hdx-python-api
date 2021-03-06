# -*- coding: UTF-8 -*-
"""Configuration Tests"""
from os.path import join

import pytest

from hdx.configuration import Configuration, ConfigurationError

try:
    FILENOTFOUND_EXCTYPE = FileNotFoundError
except:
    FILENOTFOUND_EXCTYPE = IOError

class TestConfiguration:
    @pytest.fixture(scope='class')
    def hdx_key_file(self):
        return join('tests', 'fixtures', '.hdxkey')

    @pytest.fixture(scope='class')
    def project_config_yaml(self):
        return join('tests', 'fixtures', 'config', 'project_configuration.yml')

    @pytest.fixture(scope='class')
    def project_config_json(self):
        return join('tests', 'fixtures', 'config', 'project_configuration.json')

    def test_init(self, hdx_key_file, project_config_json, project_config_yaml):
        with pytest.raises(FILENOTFOUND_EXCTYPE):
            Configuration(hdx_key_file='NOT_EXIST', project_config_yaml=project_config_yaml)

        with pytest.raises(FILENOTFOUND_EXCTYPE):
            Configuration(hdx_key_file=hdx_key_file, hdx_config_yaml='NOT_EXIST',
                          project_config_yaml=project_config_yaml)

        with pytest.raises(FILENOTFOUND_EXCTYPE):
            Configuration(hdx_key_file=hdx_key_file, hdx_config_json='NOT_EXIST',
                          project_config_yaml=project_config_yaml)

        with pytest.raises(FILENOTFOUND_EXCTYPE):
            Configuration(hdx_key_file=hdx_key_file, project_config_yaml='NOT_EXIST')

        with pytest.raises(FILENOTFOUND_EXCTYPE):
            Configuration(hdx_key_file=hdx_key_file, project_config_json='NOT_EXIST')

        with pytest.raises(ConfigurationError):
            Configuration(hdx_site='NOT_EXIST', hdx_key_file=hdx_key_file, project_config_yaml=project_config_yaml)

        with pytest.raises(ConfigurationError):
            Configuration(hdx_key_file=hdx_key_file, project_config_json=project_config_json,
                          project_config_yaml=project_config_yaml)

        with pytest.raises(ConfigurationError):
            Configuration(hdx_key_file=hdx_key_file, project_config_dict={'la': 'la'},
                          project_config_yaml=project_config_yaml)

        with pytest.raises(ConfigurationError):
            Configuration(hdx_key_file=hdx_key_file, project_config_dict={'la': 'la'},
                          project_config_json=project_config_json)

    def test_hdx_configuration_dict(self, hdx_key_file, project_config_yaml):
        actual_configuration = Configuration.create(hdx_site='prod', hdx_key_file=hdx_key_file,
                                                    hdx_config_dict={
                                                 'hdx_prod_site': {
                                                     'url': 'https://data.humdata.org/',
                                                     'username': None,
                                                     'password': None
                                                 },
                                                 'XYZ': {'567': 987}
                                             },
                                                    project_config_yaml=project_config_yaml)
        expected_configuration = {
            'api_key': '12345',
            'param_1': 'ABC',
            'hdx_prod_site': {
                'url': 'https://data.humdata.org/',
                'username': None,
                'password': None
            },
            'XYZ': {'567': 987}
        }
        assert actual_configuration == expected_configuration

    def test_hdx_configuration_json(self, hdx_key_file, project_config_yaml):
        hdx_config_json = join('tests', 'fixtures', 'config', 'hdx_config.json')
        actual_configuration = Configuration.create(hdx_key_file=hdx_key_file, hdx_config_json=hdx_config_json,
                                                    project_config_yaml=project_config_yaml)
        expected_configuration = {
            'api_key': '12345',
            'param_1': 'ABC',
            'hdx_prod_site': {
                'url': 'https://data.humdata.org/',
                'username': None,
                'password': None
            },
            'hdx_test_site': {
                'url': 'https://test-data.humdata.org/',
                'username': 'tumteetum',
                'password': 'tumteetumteetum'
            },
            'dataset': {'required_fields': [
                'name',
                'dataset_date',
            ]},
            'resource': {'dataset_id': 'package_id',
                         'required_fields': ['name', 'description'
                                             ]},
            'galleryitem': {'dataset_id': 'dataset_id', 'required_fields': [
                'dataset_id',
            ],},
        }
        assert actual_configuration == expected_configuration

    def test_hdx_configuration_yaml(self, hdx_key_file, project_config_yaml):
        hdx_configuration_yaml = join('tests', 'fixtures', 'config', 'hdx_config.yml')
        actual_configuration = Configuration.create(hdx_key_file=hdx_key_file, hdx_config_yaml=hdx_configuration_yaml,
                                                    project_config_yaml=project_config_yaml)
        expected_configuration = {
            'api_key': '12345',
            'param_1': 'ABC',
            'hdx_prod_site': {
                'url': 'https://data.humdata.org/',
                'username': None,
                'password': None
            },
            'hdx_test_site': {
                'url': 'https://test-data.humdata.org/',
                'username': 'lala',
                'password': 'lalala'
            },
            'dataset': {'required_fields': [
                'name',
                'title',
                'dataset_date',
            ]},
            'resource': {'dataset_id': 'package_id',
                         'required_fields': ['package_id', 'name', 'description'
                                             ]},
            'galleryitem': {'dataset_id': 'dataset_id', 'required_fields': [
                'dataset_id',
                'title',
            ], 'ignore_on_update': ['dataset_id']},
        }
        assert actual_configuration == expected_configuration

    def test_project_configuration_dict(self, hdx_key_file):
        actual_configuration = Configuration.create(hdx_key_file=hdx_key_file)
        expected_configuration = {
            'api_key': '12345',
            'hdx_prod_site': {
                'url': 'https://data.humdata.org/',
                'username': None,
                'password': None
            },
            'hdx_demo_site': {
                'url': 'https://demo-data.humdata.org/',
                'username': 'ZGVtbzE3OQ==',
                'password': 'ZnVud2l0aGhkeA=='
            },
            'hdx_test_site': {
                'url': 'https://test-data.humdata.org/',
                'username': 'ZGF0YXByb2plY3Q=',
                'password': 'aHVtZGF0YQ=='
            },
            'hdx_feature_site': {
                'url': 'https://feature-data.humdata.org/',
                'username': 'ZGF0YXByb2plY3Q=',
                'password': 'aHVtZGF0YQ=='
            },
            'dataset': {'required_fields': [
                'name',
                'private',
                'title',
                'notes',
                'dataset_source',
                'owner_org',
                'dataset_date',
                'groups',
                'license_id',
                'methodology',
                'data_update_frequency'
            ]},
            'resource': {'dataset_id': 'package_id',
                         'required_fields': ['package_id', 'name', 'format', 'url', 'description',
                                             'url_type', 'resource_type'
                                             ]},
            'galleryitem': {'dataset_id': 'dataset_id', 'required_fields': [
                'dataset_id',
                'title',
                'type',
                'description',
                'url',
                'image_url',
            ], 'ignore_dataset_id_on_update': True},
        }
        assert actual_configuration == expected_configuration
        actual_configuration = Configuration.create(hdx_key_file=hdx_key_file, project_config_dict={'abc': '123'})
        expected_configuration['abc'] = '123'
        assert actual_configuration == expected_configuration

    def test_project_configuration_json(self, hdx_key_file, project_config_json):
        actual_configuration = Configuration.create(hdx_key_file=hdx_key_file, project_config_json=project_config_json)
        expected_configuration = {
            'api_key': '12345',
            'hdx_prod_site': {
                'url': 'https://data.humdata.org/',
                'username': None,
                'password': None
            },
            'hdx_demo_site': {
                'url': 'https://demo-data.humdata.org/',
                'username': 'ZGVtbzE3OQ==',
                'password': 'ZnVud2l0aGhkeA=='
            },
            'hdx_test_site': {
                'url': 'https://test-data.humdata.org/',
                'username': 'ZGF0YXByb2plY3Q=',
                'password': 'aHVtZGF0YQ=='
            },
            'hdx_feature_site': {
                'url': 'https://feature-data.humdata.org/',
                'username': 'ZGF0YXByb2plY3Q=',
                'password': 'aHVtZGF0YQ=='
            },
            'my_param': 'abc',
            'dataset': {'required_fields': [
                'name',
                'private',
                'title',
                'notes',
                'dataset_source',
                'owner_org',
                'dataset_date',
                'groups',
                'license_id',
                'methodology',
                'data_update_frequency'
            ]},
            'resource': {'dataset_id': 'package_id',
                         'required_fields': ['package_id', 'name', 'format', 'url', 'description',
                                             'url_type', 'resource_type'
                                             ]},
            'galleryitem': {'dataset_id': 'dataset_id', 'required_fields': [
                'dataset_id',
                'title',
                'type',
                'description',
                'url',
                'image_url',
            ], 'ignore_dataset_id_on_update': True},
        }
        assert actual_configuration == expected_configuration

    def test_project_configuration_yaml(self, hdx_key_file, project_config_yaml):
        actual_configuration = Configuration.create(hdx_key_file=hdx_key_file, project_config_yaml=project_config_yaml)
        expected_configuration = {
            'api_key': '12345',
            'param_1': 'ABC',
            'hdx_prod_site': {
                'url': 'https://data.humdata.org/',
                'username': None,
                'password': None
            },
            'hdx_demo_site': {
                'url': 'https://demo-data.humdata.org/',
                'username': 'ZGVtbzE3OQ==',
                'password': 'ZnVud2l0aGhkeA=='
            },
            'hdx_test_site': {
                'url': 'https://test-data.humdata.org/',
                'username': 'ZGF0YXByb2plY3Q=',
                'password': 'aHVtZGF0YQ=='
            },
            'hdx_feature_site': {
                'url': 'https://feature-data.humdata.org/',
                'username': 'ZGF0YXByb2plY3Q=',
                'password': 'aHVtZGF0YQ=='
            },
            'dataset': {'required_fields': [
                'name',
                'private',
                'title',
                'notes',
                'dataset_source',
                'owner_org',
                'dataset_date',
                'groups',
                'license_id',
                'methodology',
                'data_update_frequency'
            ]},
            'resource': {'dataset_id': 'package_id',
                         'required_fields': ['package_id', 'name', 'format', 'url', 'description',
                                             'url_type', 'resource_type'
                                             ]},
            'galleryitem': {'dataset_id': 'dataset_id', 'required_fields': [
                'dataset_id',
                'title',
                'type',
                'description',
                'url',
                'image_url',
            ], 'ignore_dataset_id_on_update': True},
        }
        assert actual_configuration == expected_configuration

    def test_get_hdx_key_site(self, hdx_key_file, project_config_yaml):
        actual_configuration = Configuration.create(hdx_site='prod', hdx_key_file=hdx_key_file,
                                                    hdx_config_dict={},
                                                    project_config_yaml=project_config_yaml)
        assert actual_configuration.get_api_key() == '12345'
        assert actual_configuration.get_hdx_site_url() == 'https://data.humdata.org/'
        assert actual_configuration._get_credentials() == ('', '')

    def test_set_hdx_key_value(self, project_config_yaml):
        actual_configuration = Configuration.create(hdx_site='prod', hdx_key="TEST_HDX_KEY",
                                                    hdx_config_dict={},
                                                    project_config_yaml=project_config_yaml)
        assert actual_configuration.get_api_key() == 'TEST_HDX_KEY'
