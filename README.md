# DJANGO FILTERS STOEX

A Django app which adds storage and some extra functions to Django Filters, and requires Django Filter to be installed

Django Filters Stoex is designed to work with class based views (aka generic views) and has not been tested with DRF

# Copyright and License Information

This software contains code derived from from django_filters, to which the following copyright notice applies:

Copyright (c) Alex Gaynor and individual contributors.
All rights reserved.

The following disclaimer applies to this software and to django_filters

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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

