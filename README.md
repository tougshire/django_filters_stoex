# DJANGO FILTERS STOEX

A Django app which adds storage and some extra functions to Django Filters, and requires Django Filter to be installed

Django Filters Stoex is designed to work with class based views (aka generic views) and has not been tested with DRF

# Copyright and License Information

This software contains code derived from from django_filters, to which the following copyright notice applies:

Copyright (c) Alex Gaynor and individual contributors.
All rights reserved.

This software is licensed under the BSD 3-Clause "New" or "Revised" License, a copy of which is included in this repository

## Description

* Allows authenticated users to save filters in the database
* Defines a cross-field filter to allow for searching text in multiple fields
* Allows use of touglates multiple select widget

## Getting Started

### Dependencies

* Touglates: [https://github.com/tougshire/touglates](https://github.com/tougshire/touglates).
* Django Filters: [https://pypi.org/project/django-filter/](https://pypi.org/project/django-filter/)
* This repository, Django FIlters Stoex: [https://github.com/tougshire/django_filters_stoex](https://github.com/tougshire/django_filters_stoex)

### Installing

* Start a Django Project
* From your project root folder (the one with manage.py in it), clone Django Filters Stoex and Touglates using git
* * ex:
* * * `git clone https://github.com/tougshire/touglates`
* * * `git clone https://github.com/tougshire/django_filters_stoex`

* Install Django Filters with pip
* * ex: pip install django-filter

### Configuring

#### In settings.py

```
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tougshire_auth.apps.TougshireAuthConfig",
    "touglates.apps.TouglatesConfig",
    "django_filters",
    "django_filters_stoex.apps.DjangoFiltersStoexConfig",
    "app_your_using_to_list_objects.apps.AppYourUsingToListObjectsConfig
]
```

#### In yourapp.filterset.py

Define filters in a similar way that you would using django_filters

In order to save a filter, you must define a field for the filter name.

```
class ExampleFilter(django_filters.FilterSet):
    filterset_name = forms.CharField()

```
#### In yourapp.yourmodel_filter.html

##### Messages

You should have a way of displaying messages.
```
{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
    {% endfor %}
</ul>
{% endif %}
```
## Help

This is still in early phases and much more has to be done.

## Author

benjamin at tougshire.com

