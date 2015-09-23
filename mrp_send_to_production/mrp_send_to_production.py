# -*- encoding: utf-8 -*-
from openerp import models, fields, api, _
import pdb

class mrp_production(models.Model):
    _inherit = 'mrp.production'
    
    STATE_SELECTION = [
        ('draft', 'New'),
        ('confirmed', 'Send to Production'),
        ('to_production', 'Awaiting Raw Materials'),
        ('ready', 'Ready to Produce'),
        ('in_production', 'Production Started'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ]
    state = fields.Selection(selection=STATE_SELECTION, string='Status', required='True',default='draft', track_visibility='onchange')
    
    @api.one
    def action_send_to_production(self):
        self.state='to_production'
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: 
