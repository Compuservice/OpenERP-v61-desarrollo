# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################

from osv import fields, osv
import time

class formacion_contacts(osv.osv):
    _name = "res.partner.address"
    _inherit = "res.partner.address"
    _columns = {
        'apodo' : fields.char('Apodo', size=20),        
        'nombre' : fields.char('Nombre', size=20),
        'apellidos': fields.char('Apellidos', size=20),
        'fecha_contacto' : fields.date('Fecha', help='Fecha en la que se produjo el contacto'),
        'motivo': fields.text('Motivo'),
        'tags' : fields.text('Tags'),
        'is_contacto': fields.boolean('Contacto'),
    }
    _defaults =  {
        'is_contacto': lambda self, cr, uid, context: context.get('is_contacto', False),
        'fecha_contacto' : lambda *a : time.strftime("%Y-%m-%d"),
    }
    def onchange_nomyapel(self, cr, uid, ids, nom,apel):
        v = {}
        # Si se modifican nombre o apellidos se asignan al campo name original de OpenERP
        if nom and nom!='':
            nom = nom.encode('utf-8','replace')
            if apel and apel!='':
                apel = apel.encode('utf-8','replace')
                v = {'name':str(nom) + ' ' + str(apel), }
            else:
                v = {'name':nom, } 
        return {'value': v}

formacion_contacts()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
