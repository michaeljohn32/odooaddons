.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==============
procurement_location_per_contract
==============

This module was written to extend the functionality of of the warehouse to support creation of locations based on contracts.  
When a sales order is created for a contract, it will procure items to a new location that matches the contract name (if the location doesn't already exist).

Installation
============

To install this module, you need to:

install from Odoo interface

Configuration
=============

To configure this module, you need to have the following:

* "Manage Advanced Routes" checked in Warehouse settings
* Outgoing Method on the warehouse needs to be Pick & Ship (to be fixed)
* Stock MTS+MTO configured on the warehouse

Usage
=====

To use this module, you need to:


Known issues / Roadmap
======================

* remove Pick & Ship dependency
* remove MTS+MTO dependency

Bug Tracker
===========

Credits
=======

Contributors
------------

* John Walsh <michaeljohn32@yahoo.com>

Maintainer
----------
