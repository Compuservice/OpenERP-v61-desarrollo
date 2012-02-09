# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2007-Today  All Rights Reserved.

#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

{
    "name": "Formacion",
    "version": "0.1",
    "category" : "Generic Modules/Formación",
    'depends': ['base', 'document', 'l10n_es_toponyms', 'l10n_es_toponyms_region', 'account_payment_extension'],
    "author": "www.compuservice.es",
    "category": "Training",
    "description":
    """
        Módulo para la gestión de un centro de formación, que incorpora las siguientes características:
            * Extiende la clase res.partner añadiendo los campos necesarios para gestionar entidades, cursos, docentes y alumnos.
            * Crea el objeto cursos
        
    """,
    "init_xml": [],
    'update_xml': [
                   'formacion_view.xml',
		'formacion_partner.xml',
        'formacion_menus.xml',
        'workflow/workflow_formacion_cursos.xml',
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}
