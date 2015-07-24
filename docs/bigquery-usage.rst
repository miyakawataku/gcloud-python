.. toctree::
  :maxdepth: 0
  :hidden:

BigQuery
========

Authorization / Configuration
-----------------------------

- Use :class:`Client <gcloud.bigquery.client.Client>` objects to configure
  your applications.

- :class:`Client <gcloud.bigquery.client.Client>` objects hold both a ``project``
  and an authenticated connection to the PubSub service.

- The authentication credentials can be implicitly determined from the
  environment or directly via
  :meth:`from_service_account_json <gcloud.bigquery.client.Client.from_service_account_json>`
  and
  :meth:`from_service_account_p12 <gcloud.bigquery.client.Client.from_service_account_p12>`.

- After setting ``GOOGLE_APPLICATION_CREDENTIALS`` and ``GCLOUD_PROJECT``
  environment variables, create an instance of
  :class:`Client <gcloud.bigquery.client.Client>`.

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client()

- Override the credentials inferred from the environment by passing explicit
  ``credentials`` to one of the alternative ``classmethod`` factories,
  `:meth:gcloud.bigquery.client.Client.from_service_account_json`:

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client.from_service_account_json('/path/to/creds.json')

  or `:meth:gcloud.bigquery.client.Client.from_service_account_p12`:

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client.from_service_account_p12('/path/to/creds.p12', 'jrandom@example.com')


Projects
--------

A project is the top-level container in the ``BigQuery`` API:  it is tied
closely to billing, and can provide default access control across all its
datasets.  If no ``project`` is passed to the client container, the library
attempts to infer a project using the environment (including explicit
environment variables, GAE, and GCE).

To override the project inferred from the environment, pass an explicit
``project`` to the constructor, or to either of the alternative
``classmethod`` factories:

  .. doctest::

     >>> from gcloud import bigquery
     >>> client = bigquery.Client(project='PROJECT_ID')

Project ACLs
~~~~~~~~~~~~

Each project has an access control list granting reader / writer / owner
permission to one or more entities.  This list cannot be queried or set
via the API:  it must be managed using the Google Developer Console.

Datasets
--------

A dataset represents a collection of tables, and applies several default
policies to tables as they are created:

- An access control list (ACL).  When created, a dataset has an ACL
  which maps to the ACL inherited from its project.

- A default table expiration period.  If set, tables created within the
  dataset will have the value as their expiration period.

Dataset operations
~~~~~~~~~~~~~~~~~~

Create a new dataset for the client's project:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.create()  # API request

Check for the existence of a dataset:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.exists()  # API request
   True

List datasets for the client's project:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> datasets, next_page_token = client.list_datasets()  # API request
   >>> [dataset.name for dataset in datasets]
   ['dataset_name']

Refresh metadata for a dataset (to pick up changes made by another client):

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.reload()  # API request

Patch metadata for a dataset:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> one_day_ms = 24 * 60 * 60 * 1000
   >>> dataset.patch(description='Description goes here',
   ...               default_table_expiration_ms=one_day_ms)  # API request

Replace the ACL for a dataset, and update all writeable fields:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.get()  # API request
   >>> acl = list(dataset.acl)
   >>> acl.append(bigquery.Access(role='READER', entity_type='domain', entity='example.com'))
   >>> dataset.acl = acl
   >>> dataset.update()  # API request

Delete a dataset:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.delete()  # API request


Tables
------

Tables exist within datasets.  List tables for the dataset:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> tables, next_page_token = dataset.list_tables()  # API request
   >>> [table.name for table in tables]
   ['table_name']

Create a table:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> table.create()  # API request

Check for the existence of a table:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> table.exists()  # API request
   True

Refresh metadata for a table (to pick up changes made by another client):

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> dataset.reload()  # API request

Patch specific properties for a table:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> table.patch(friendly_name='Person Ages',
   ...             description='Ages of persons')  # API request

Update all writable metadata for a table

.. doctest::

   >>> from gcloud import bigquery
   >>> from gcloud.bigquery import SchemaField
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> table.schema = [
   ...     SchemaField(name='full_name', type='string', mode='required'),
   ...     SchemaField(name='age', type='int', mode='required)]
   >>> table.update()  # API request

Delete a table:

.. doctest::

   >>> from gcloud import bigquery
   >>> client = bigquery.Client()
   >>> dataset = client.dataset('dataset_name')
   >>> table = dataset.table(name='person_ages')
   >>> table.delete()  # API request