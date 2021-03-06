###################################################################################
#
#    Copyright (C) 2018 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

import logging

from odoo import api, models, fields

_logger = logging.getLogger(__name__)

class Base(models.AbstractModel):
    
    _inherit = 'base'

    @api.multi
    def unlink(self):
        oids = []
        for name in self._fields:
            field = self._fields[name]
            if field.type == 'lobject' and field.store:
                for record in self:
                    oid = record.with_context({'oid': True})[name]
                    if oid:
                        oids.append(oid)
        super(Base, self).unlink()
        for oid in oids:
            self.env.cr._cnx.lobject(oid, 'rb').unlink()