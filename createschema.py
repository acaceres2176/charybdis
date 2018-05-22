#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pprint

_solr_schema_url = 'http://localhost:8983/solr/credentials/schema'


def add_fields():
    """
    Add all fields to Solr schema.

    :returns: bool
    :raises: Request.Exception
    """
    fields = [
        {
            'name': 'id',
            'type': 'string',
            'stored': True,
            'uniqueKey': True

        },
        {
            'name': 'username',
            'type': 'string',
            'stored': True

        },
        {
            'name': 'password',
            'type': 'string',
            'stored': True
        },
        {
            'name': 'domain',
            'type': 'string',
            'stored': True
        },
    ]

    for field in fields:
        add_field(field)

    return True


def add_field(field):
    """
    Add field to Solr schema.

    :param field: dictionary contain field definition
    :returns: Requests.Response.
    :raises: Request.Exception
    """
    data = {
        'add-field': field
    }
    r = requests.post(_solr_schema_url, json=data)
    r.raise_for_status()
    print('{}: {}'.format(field, r.status_code))
    return r


def view_schema():
    r = requests.get(_solr_schema_url)
    r.raise_for_status()
    pprint.pprint(r.json())


if __name__ == '__main__':
    add_fields()
    print('Successfully created schema')
    # view_schema()
