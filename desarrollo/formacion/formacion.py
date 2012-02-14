# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2007-Today MALAGATIC (http://www.malagatic.com) All Rights Reserved.
#                       Juanjo Algaz (juanjoa@malagatic.com)

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

from osv import osv, fields
import datetime
import time



class formacion_configuracion_cursos(osv.osv):
    _name = 'formacion.configuracion.cursos'
    _columns = {
                'name':fields.char('Nombre', size=64, required=True),
                }
formacion_configuracion_cursos()


class formacion_cursos(osv.osv):
    MODALIDADES = [
                   ('1', 'Teleformación'),
                   ('2', 'Presencial'),
                   ('3', 'Mixta'),
                   ('4', 'Distancia'),
                   ]
    
    _name = 'formacion.cursos'
    _columns = {
                'name':fields.many2one('formacion.configuracion.cursos', 'Nombre del curso', required=True),
                'modalidad': fields.selection(MODALIDADES, 'Modalidad'),
                'horas': fields.integer('Horas'),
                'horas_presenciales': fields.integer('Horas Presenciales'),
                'horas_teleformacion': fields.integer('Horas Teleformación'),
                'fecha_inicio': fields.datetime('Fecha Inicio'),
                'fecha_fin': fields.datetime('Fecha Finalización'),
                'log_fecha_creacion': fields.datetime('Fecha Creación'),
                'log_fecha_abierto': fields.datetime('Fecha Apertura'),
                'log_fecha_impartiendo': fields.datetime('Fecha Impartición'),
                'log_fecha_cerrando': fields.datetime('Fecha Cierre'),
                'log_fecha_cerrado': fields.datetime('Fecha Cerrado'),
                'log_fecha_cancelado': fields.datetime('Fecha Cancelación'),
                'fecha_fin': fields.datetime('Fecha Finalización'),              
                #Relaciones
                'centro_id':fields.many2one('res.partner','Entidad Impartidora', required=True, domain=[('is_entidad','=',True)]),
                'direccion_id': fields.many2one('res.partner.address','Dirección'),
                'company_id': fields.many2one('res.company', 'Company', select=1),
                'alumnos_ids': fields.many2many('res.partner', 'formacion_alcu_rel', 'id_curso', 'id_alumno', 'Relación de alumnos', domain=[('is_alumno','=',True)]), 
                'docentes_ids': fields.many2many('res.partner', 'formacion_docu_rel', 'id_curso', 'id_docente', 'Relación de docentes', domain=[('is_docente','=',True)]),
                #'entidades_ids': fields.many2many('res.partner', 'formacion_encu_rel', 'id_curso', 'id_entidad', 'Relación de entidades', domain=[('is_entidad','=',True)]),
                #'docente_id':fields.many2one('res.partner', 'Docente'),
                'tags' : fields.text('Tags'),                
                'notas': fields.text('Observaciones'),
                'state': fields.selection([
                    ('draft', 'Borrador'),
                    ('open', 'Autorizado'),
                    ('studying', 'Cursando'),
                    ('closing', 'Cerrando'),
                    ('closed', 'Cerrado'),
                    ('cancel', 'Cancelado')], 'Estado', readonly=True,
            help='*Borrador: Recien creado. \
            \n*Autorizado: una vez autorizado el curso. \
            \n*Cursando: para los cursos que se están impartiendo. \
            \n*Cerrando: con el curso terminado y gestionando el cierre total. \
            \n*Cerrado: para el curso impartido y con la documentación completada'
            ),
        	'file_ids': fields.one2many('ir.attachment','res_id', 'Documentos'),
                
                }
    _defaults = {
        'centro_id': lambda self, cr, uid, context: context.get('centro_id', False),
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'formacion.configuracion.cursos.nomnres', context=c),
        'modalidad': lambda *a: '1',
                 }
    
    
    def formacion_cursos_draft(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state': 'draft','log_fecha_creacion': time.strftime('%Y-%m-%d %H:%M:%S') })
        return True

    def formacion_cursos_open(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state': 'open' ,'log_fecha_abierto': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def formacion_cursos_impartiendo(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state': 'studying' ,'log_fecha_impartiendo': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True
    
    def formacion_cursos_cerrando(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state': 'closing' ,'log_fecha_cerrando': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def formacion_cursos_close(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state': 'closed' ,'log_fecha_cerrado': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

    def formacion_cursos_cancelar(self, cr, uid, ids):
        self.write(cr, uid, ids, { 'state': 'cancel' ,'log_fecha_cancelado': time.strftime('%Y-%m-%d %H:%M:%S')})
        return True

formacion_cursos()
    
