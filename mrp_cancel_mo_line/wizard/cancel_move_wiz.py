# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime
import pdb

class cancel_move_wiz(models.TransientModel):
    _name = 'mrp_cancel_mo_line.cancel_move_wiz'
    _description = 'Cancel a Manufacturing Order Line'

    @api.multi
    def cancel_move(self):
        '''
            Cancels a Move 
        '''
        # Need to ensure it is one since we are in an action
        pdb.set_trace()
        self.ensure_one()

        move = self.env['stock.move'].browse(self.env.context['active_id'])
        move.action_cancel()
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:  
