# -*- coding: utf-8 -*-
# © 2015 John Walsh michaeljohn32@yahoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api
import pdb
class StockLocation(models.Model):
  _inherit = 'stock.location'
  project_id = fields.Many2one(comodel_name='account.analytic.account', string='Contract/Analytic',help="This location groups products to a contract-specific location in the warehouse")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
