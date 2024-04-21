# DJANGO FILTERS STOEX

A Django app which adds storage and some extra functions to Django Filters, and requires Django Filter to be installed

Django Filters Stoex is designed to work with class based views (aka generic views) and has not been tested with DRF


## Description

* Allows authenticated users to save filters in the database
* Defines a cross-field filter to allow for searching text in multiple fields

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
## Help

This is still in early phases and much more has to be done.

## Author

benjamin at tougshire.com

