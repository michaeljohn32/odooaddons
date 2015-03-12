Odoo Addons
===========

This repository hosts a few different addons for use in odoo v.8


"mrp_bom_calculation"
====================
This addon calculates the "real" cost of a Bill of Materials within Odoo as
the item is produced using cost of each of the reserved quantities

When a user "consumes" a product, a boolean flag is set that that particular
move needs to be costed later

Finally, when a new item is "Produced":
- We add up the material cost of all subproducts
- Update the Product's cost with the value just obtained
