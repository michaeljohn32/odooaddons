# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api
from datetime import datetime

class cancel_move_wiz(models.TransientModel):
    _name = 'mrp_cancel_mo_line.cancel_move_wiz'
    _description = 'Cancel a Manufacturing Order Line'

    @api.multi
    def cancel_move(self):
        '''
            Cancels a Move 
        '''
        # Need to ensure it is one since we are in an action
        self.ensure_one()

        move = self.env['stock.move'].browse(self.env.context['active_id'])
        move.action_cancel()
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:  
