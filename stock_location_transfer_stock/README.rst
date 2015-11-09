.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
stock_location_transfer_stock
==============

This module adds an option to the "More" dropdown of the Warehouse locations list view
called "Tranfer Stock from Selected Locations." If you select one or more locations
and click this option, it will create a one picking per selected location moving
all unreserved stock to the destination location you specify.

Installation
============

To install this module, you need to:

* put the stock_location_transfer_stock directory into an addons directory 
  that Odoo can read
* Update your Module list
* Find and Install 'stock_location_transfer_stock'

Configuration
=============

To configure this module, you need to:

* do nothing after install

Usage
=====

To use this module, you need to:
* Select one or more location from the "locations" view of Odoo
* Click the "More" dropdown
* Select "Transfer Stock from Selected Locations"
* Select the destination location in the window that appears
* Click the "Create Pickings" button
* Transfer the stock using normal transfer process

Known issues / Roadmap
======================

* Leaves reserved quants in the stock location.  This is by design.
* Does not create a picking if there is no unreserved stock.
* returns an empty tree view if there is no stock in all locations to transfer

Bug Tracker
===========

Credits
=======

Contributors
------------

* John Walsh michaeljohn32@yahoo.com

Maintainer
----------
