=======================
Core Explore Oaipmh App
=======================

OAI-PMH exploration functions for curator core project.

Quick start
===========

1. Add "core_explore_oaipmh_app" to your INSTALLED_APPS setting
---------------------------------------------------------------

.. code:: python

    INSTALLED_APPS = [
      ...
      'core_explore_oaipmh_app',
    ]

2. Add "core_explore_oaipmh_app" to your DATA_SOURCES_EXPLORE_APPS setting
--------------------------------------------------------------------------

.. code:: python

    DATA_SOURCES_EXPLORE_APPS = [
        'core_explore_oaipmh_app',
    ]

3. Include the core_explore_oaipmh_app URLconf in your project urls.py
----------------------------------------------------------------------

.. code:: python

        url(r'^oaipmh_search/', include("core_explore_oaipmh_app.urls")),
