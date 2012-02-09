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

class formacion_partner(osv.osv):
    _name= "res.partner"
    _inherit = "res.partner"
    _columns = {
        # Tipo de partner
        'is_alumno' : fields.boolean('Alumno', help='Es un alumno'),
        'is_docente' : fields.boolean('Docente', help='Es un docente'),
        'is_entidad' : fields.boolean('Entidad', help='Es una entidad'),
        
         # Relaciones
        #'alumnos_ids': fields.many2many('res.partner', 'formacion_alen_rel', 'id_entidad', 'id_alumno', 'Relación de alumnos', domain=[('is_alumno','=',True)]), #Será visible en entidades
        'entidades_al_ids' : fields.many2many('res.partner', 'formacion_alen_rel', 'id_alumno', 'id_entidad', 'Relación de alumnos con entidades' ,domain=[('is_entidad','=',True)]), #será visible en alumnos
        'entidades_do_ids' : fields.many2many('res.partner', 'formacion_doen_rel', 'id_docente', 'id_entidad', 'Relación de docentes con entidades' ,domain=[('is_entidad','=',True)]), #será visible en docentes
        'cursos_al_ids' : fields.many2many('formacion.cursos', 'formacion_alcu_rel', 'id_alumno', 'id_curso', 'Relación de alumnos con cursos'), #será visible en alumnos
        'cursos_en_ids' : fields.one2many('formacion.cursos', 'centro_id', 'Relación de cursos',),
        #'cursos_en_ids' : fields.many2many('formacion.cursos', 'formacion_encu_rel', 'id_entidad', 'id_curso', 'Relación de cursos'), #será visible en entidades
        'cursos_do_ids' : fields.many2many('formacion.cursos', 'formacion_docu_rel', 'id_docente', 'id_curso', 'Relación de cursos'), #será visible en docentes

        # Datos compartidos por docentes y alumnos
        'nombre': fields.char('Nombre', size=20),
        'apellidos': fields.char('Apellidos', size=20),
        'dni' : fields.char('DNI', size=9, help='Documento nacional de identidad'),
        'foto': fields.binary('Foto'), # Docentes y ¿alumnos?
        
        # Datos compartidos por alumnos y entidades
        'forma_pago' : fields.many2one('payment.type', 'Forma de pago'),
        'comprobante_pago' : fields.boolean('Comprobante de pago'),
        
        # Datos compartidos por entidades y docentes
        'tags' : fields.text('Tags'),

        # Datos específicos de entidades
        'ftfe' : fields.boolean('FTFE', help='Fundación Tripartita para la Formación en el Empleo'),
        #TODO 'factura' : fields.('¿Que es?')

        # Datos específicos de alumnos
        'fecha_nacimiento' : fields.date('Fecha de nacimiento',),
        'fecha_inscripcion' : fields.date ('Fecha inscripción'),
        'fecha_matricula' : fields.date ('Fecha matriculación'),
        'situacion_laboral' : fields.selection ([(1,'Estudiante'),(2,'Desempleado'),(3,'Autónomo'),(4,'Ocupado - FTFE'),(99,'Otra o desconocida')],'Situación laboral'),
        'factura_al' : fields.selection ([(1,'Individual'),(2,'Entidad')],'Factura'), #Alumnos

        # Datos específicos de docentes
        'especialidades': fields.text('Especialidades'),
        'formacion': fields.text('Formación'),
        'exp_laboral': fields.text('Experiencia laboral'),
        'exp_docente': fields.text('Experiencia docente/CAP'),
        'cv_adjunto': fields.binary('Curriculum vitae'),
            # Lista de compromisos
        'lista_chk1': fields.boolean('Manual de estilo'),
        'lista_chk2': fields.boolean('Guía de marcado'),
        'lista_chk3': fields.boolean('Guía de programación didáctica'),
        'lista_chk4': fields.boolean('Guía de elaboración de screencats y vídeos'),
        'lista_chk5': fields.boolean('Acuerdo de cesión de derechos'),
        'lista_chk6': fields.boolean('Contrato laboral privado'),

        # Para visualizar en la vista de árbol
        'movil': fields.related('address', 'mobile', type='char', string='Móvil'),
        'cpostal': fields.related('address', 'zip', type='char', string='Código Postal'),

        #######################################################################################################
        # *Documentos*
        #######################################################################################################
        'file_ids': fields.one2many('ir.attachment','res_id', 'Documentos'),

    }

    def dni_ok(self,cr,uid,ids):
        for objeto in self.browse(cr, uid, ids):
            if objeto.dni:
                if len(objeto.dni)==9:
                    try: numero = int(objeto.dni[0:8])
                    except: return False
                    NIF='TRWAGMYFPDXBNJZSQVHLCKE'
                    letra_correcta = NIF[numero%23]
                    letra = objeto.dni[8]
                    if letra == letra_correcta: return True
                    else: return False
            else: return True
        return False

    #_constraints = [(dni_ok,'El DNI no es correcto', ['dni'])]

    _defaults =  {
        'is_alumno': lambda self, cr, uid, context: context.get('is_alumno', False),
        'is_docente' : lambda self, cr, uid, context: context.get('is_docente', False),
        'is_entidad' : lambda self, cr, uid, context: context.get('is_entidad', False),

    }
formacion_partner()

class funciones_formacion_partner(osv.osv):
    # Funciones 'on_change' añadidas a res.partner
    _inherit ="res.partner"
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

    def onchange_checkdni(self, cr, uid, ids, dni):
        dniok = False
        try:
            try: numero = int(dni[:-1])
            except: dniok = False
            NIF='TRWAGMYFPDXBNJZSQVHLCKE'
            letra_correcta = NIF[numero%23]
            letra = dni[len(dni)-1].upper()
            if letra == letra_correcta: dniok = True
            else: dniok = False
            if dniok:
                return {'value':{'vat':'ES'+dni}}
            else:
                return {'warning':{'title':'Atención','message':'El DNI no es correcto.'}}
        except: return True #dni vacio

funciones_formacion_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
