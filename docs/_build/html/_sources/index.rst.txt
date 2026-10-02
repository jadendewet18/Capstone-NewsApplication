Welcome to Capstone News Application's documentation!
=====================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Database & Environment Configuration
====================================
The application dynamically configures its database settings using environment
variables. When deployed via Docker Compose, these variables are injected into
the web container to establish a connection with the MySQL database service.

Available Environment Variables:
  - ``DB_NAME``: Name of the MySQL database (default: ``news_db``)
  - ``DB_USER``: Database username (default: ``root``)
  - ``DB_PASSWORD``: Database password (default: ``""``)
  - ``DB_HOST``: Database host address (default: ``127.0.0.1``)
  - ``DB_PORT``: Database port (default: ``3306``)

News App Models
===============
.. automodule:: news_app.models
   :members:
   :undoc-members:
   :show-inheritance:

News App Views
==============
.. automodule:: news_app.views
   :members:
   :undoc-members:
   :show-inheritance: