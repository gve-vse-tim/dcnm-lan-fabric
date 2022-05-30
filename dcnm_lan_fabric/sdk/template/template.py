#!/usr/bin/env python3
"""
Copyright (c) 2022 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Dr Timothy E Miller <timmil@cisco.com>"
__contributors__ = [
]
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"


import json
from typing import List, Any


class template_parameter:
    def __init__(self, param_data):
        self = param_data  # noqa: F841

    def __getattribute__(self, __name: str) -> Any:
        return self.__data.get(__name)

    def __delattr__(self, __name: str) -> None:
        del self.__data[__name]

    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__data[__name] = __value

    def name(self):
        return self['name']

    def description(self):
        return self['description']

    def summary(self):
        return "{0:25}: {1}".format(
            self.name(), self.description()
        )

    def metaproperties(self):
        return self.__data.get('metaProperties', None)

    def annotations(self):
        return self.__data.get('annotations', None)

    def nvpair(self):
        meta = self.metaproperties()
        notes = self.annotations()

        required = notes.get('IsMandatory', False)

        if not meta:
            return (self['name'], None, required)

        return (
            self.name,
            meta.get('defaultValue', None, required)
        )


class template:
    def __init__(self, tmpl_data):
        self.__data = tmpl_data
        self.name = tmpl_data.get('name', 'Unknown')
        self.description = tmpl_data.get('description', 'Unknown')
        self.supported_platforms = tmpl_data.get('supportedPlatforms', 'Unknown')  # noqa:E501
        self.template_type = tmpl_data.get('templateType', 'Unknown')
        self.template_subtype = tmpl_data.get('templateSubType', 'Uknown')
        self.content_type = tmpl_data.get('contentType', 'Unknown')

        parameters = tmpl_data.get('parameters', list())
        self.parameters: List[template_parameter] = list()

        for p in parameters:
            self.parameters.append(template_parameter(p))

    def __str__(self):
        return f"dcnm/ndfc.template {self.name}"

    def summary(self):
        return f"{self.name:25}: {self.description}"

    def brief(self):
        output = list()

        output.append(f"Name: {self.name}")
        output.append(f"Description: {self.description}")
        output.append(f"Template Type: {self.template_type}")
        output.append(f"Template SubType: {self.template_subtype}")
        output.append(f"Content Type: {self.content_type}")
        output.append(f"Supported Platforms: {self.supported_platforms}")

        return "\n".join(output)

    def verbose(self):
        return json.dumps(self.__data, indent=4)

    def nvpairs(self):
        pairs = list()
        for attr in self.parameters:
            pairs.append(attr.nvpair())
        pass


def get_all_templates(api, filter):
    list_of_templates = api.get_templates(filter)
    sorted_list = sorted(list_of_templates, key=lambda tmpl: tmpl['name'])

    # Generate objects
    list_of_templates = [template(tmpl) for tmpl in sorted_list]

    return list_of_templates


def get_template(api, name, populate=True):
    tmpl_data = api.get_template_by_name(name, populate)
    return template(tmpl_data)
