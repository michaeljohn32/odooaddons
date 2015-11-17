# -*- coding: utf-8 -*-
# © 2015 John Walsh michaeljohn32@yahoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "procurement_location_per_contract",
    "summary": "Set up all procurements under a contract to be bought/manufactured in that location",
    "version": "8.0.1.0.0",
    "category": "Inventory",
    "website": "https://github.com/michaeljohn32/",
    "author": "John Walsh michaeljohn32@yahoo.com",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "account_analytic_analysis", # Adds the contract to the SO
        "sale",
        "stock_mts_mto_rule",
    ],
    "data": [
        "data/stock_data.xml"
    ],
    "demo": [
        "demo/demo.xml"
    ],
}
