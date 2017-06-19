# core_explore_oaipmh_app

core_explore_oaipmh_app is a Django app.

# Quick start

1. Add "core_explore_oaipmh_app" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
  ...
  'core_explore_oaipmh_app',
]
```

2. Add "core_explore_oaipmh_app" to your DATA_SOURCES_EXPLORE_APPS setting like this:

```python
DATA_SOURCES_EXPLORE_APPS = [
    'core_explore_oaipmh_app',
]
```


3. Include the core_explore_oaipmh_app URLconf in your project urls.py like this::

```python
    url(r'^oaipmh_search/', include("core_explore_oaipmh_app.urls")),
```
