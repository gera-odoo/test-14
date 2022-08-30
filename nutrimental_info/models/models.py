# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NutrInfo(models.Model):
    _name = 'nutrimental.info'
    _description = 'Nutrimental Info'
    _rec_name = 'nutriment_id'
    _order = 'sequence'

    nutriment_id = fields.Many2one('nutrimental.value', string="Nutriment", index=True)
    sequence = fields.Integer(string="Sequence")
    value = fields.Float(string="Value", digits=(12, 4))
    uom_id = fields.Many2one('uom.uom', string="Unit of measure", compute="get_default_uom", inverse="_pass",
                             store=True)
    product_id = fields.Many2one('product.product', string="Product")
    group_id = fields.Many2one('nutrimental.group', related="nutriment_id.group_id", store=True,
                               string="Classification")
    quantity = fields.Float(string="Quantity per size", digits=(12, 4), compute="get_qty_size", store=True,
                            inverse="_pass")
    additional_info = fields.Char(string="Additional info")
    second_quantity = fields.Float(string="Quantity per size", digits=(12, 4), compute="get_second_qty_size",
                                   store=True,
                                   inverse="_pass")
    additional_info_second = fields.Char(string="Additional info")
    nutrimental_reference = fields.Many2one('nutrimental.needs.line', string="Reference")
    second_nutrimental_reference = fields.Many2one('nutrimental.needs.line', string="Reference")
    reference_value = fields.Float(string="% (Reference value", compute="get_ref_value", inverse="_pass", store=True)
    second_reference_value = fields.Float(string="% (Reference value", compute="get_second_ref_value", inverse="_pass",
                                          store=True)

    @api.depends('quantity', 'nutrimental_reference.reference_value')
    def get_ref_value(self):
        for info in self:
            if info.quantity and info.nutrimental_reference.reference_value:
                info.write({'reference_value': (info.quantity / info.nutrimental_reference.reference_value) * 100})
            else:
                info.write({'reference_value': False})

    @api.depends('quantity', 'second_nutrimental_reference.reference_value')
    def get_second_ref_value(self):
        for info in self:
            if info.second_quantity and info.second_nutrimental_reference.reference_value:
                info.write({'second_reference_value': (
                                                              info.second_quantity / info.second_nutrimental_reference.reference_value) * 100})
            else:
                info.write({'reference_value': False})

    def _pass(self):
        pass

    @api.depends('value', 'product_id.second_size')
    def get_second_qty_size(self):
        for info in self:
            if info.product_id.second_size and info.value and info.uom_id.is_percentage:
                info.write({'second_quantity': (info.value * info.product_id.second_size) / 100})
            elif info.product_id.second_size and info.value and not info.uom_id.is_percentage:
                info.write({'second_quantity': (info.value * info.product_id.second_size)})
            else:
                info.write({'second_quantity': False})

    @api.depends('value', 'product_id.size')
    def get_qty_size(self):
        for info in self:
            if info.product_id.size and info.value and info.uom_id.is_percentage:
                info.write({'quantity': (info.value * info.product_id.size) / 100})
            elif info.product_id.size and info.value and not info.uom_id.is_percentage:
                info.write({'quantity': (info.value * info.product_id.size)})
            else:
                info.write({'quantity': False})

    @api.depends('nutriment_id')
    def get_default_uom(self):
        for record in self:
            if record.nutriment_id.uom_id:
                record.uom_id = record.nutriment_id.uom_id.id
            else:
                record.uom_id = False


class Product(models.Model):
    _inherit = 'product.product'

    nutrimental_ids = fields.One2many('nutrimental.info', 'product_id', string="Nutrimental info")
    display_nutrimental_info = fields.Boolean(related="categ_id.display_nutrimental_info",
                                              string="Display nutrimental info?")
    size = fields.Float(string="Size per portion")
    size_uom_id = fields.Many2one('uom.uom', string="Measure of size per portion", help="Measure of size per portion")
    servings_per_container = fields.Float(string="Servings per container")
    additional_servings_info = fields.Char(string="Additional info")
    has_second_servings = fields.Boolean(string="Has second serving?")
    second_servings_per_container = fields.Float(string="Servings per container")
    second_additional_servings_info = fields.Char(string="Additional info")
    second_size = fields.Float(string="Size per portion")
    second_size_uom_id = fields.Many2one('uom.uom', string="Measure of size per portion",
                                         help="Measure of size per portion")
    other_ingredients = fields.Text(string="Other Ingredients")
    recommended_use = fields.Text(placeholder='Recommended Use...', string="Recommended Use")
    additional_claim = fields.Text(placeholder="Aditional info", string="Additional information",
                                   help="Claim for label")


class ProductCateg(models.Model):
    _inherit = 'product.category'

    display_nutrimental_info = fields.Boolean(string="Display nutrimental info?")


class ProductUom(models.Model):
    _inherit = 'uom.uom'

    is_percentage = fields.Boolean(string="% per size",
                                   help="Displays if the unit should be considered as a percentage")


class Nutriment(models.Model):
    _name = 'nutrimental.value'
    _description = 'Nutriment'
    _rec_order = 'sequence'
    _rec_name = 'display_name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", store=True, default=True)
    display_name = fields.Char(string="Display Name", compute="_compute_complete_name", store=True, index=True)
    code = fields.Char(string="Code", help="Short name used to identify the nutrimental value")
    sequence = fields.Integer(string="Sequence", help="Sequence to choose the order of the nutriments")
    group_id = fields.Many2one('nutrimental.group', string="Classification")
    uom_id = fields.Many2one('uom.uom', string="Default unit of measure")

    @api.depends('name', 'code')
    def _compute_complete_name(self):
        for record in self:
            if record.name and record.code:
                record.display_name = '%s / %s' % (record.code, record.name)
            else:
                record.display_name = False


class NutrimentGroup(models.Model):
    _name = 'nutrimental.group'
    _description = 'Nutrimental group'

    name = fields.Char(string="Name")
    value_ids = fields.One2many('nutrimental.value', 'group_id', string="Nutriments")


class Needs(models.Model):
    _name = 'nutrimental.needs'
    _description = 'Needs group'

    need_line_ids = fields.One2many(comodel_name='nutrimental.needs.line', inverse_name='need_id',
                                    string="Specific needs", required=True)
    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    based_on = fields.Text(string="Based On",
                           help="Used to display the computations the needs are based on, for the computation of every value use X")


class NeedsLine(models.Model):
    _name = 'nutrimental.needs.line'
    _description = 'Nutrimental needs specifications'
    _rec_name = 'code'

    nutriment_ids = fields.Many2many('nutrimental.value', string="Nutriment", index=True)
    code = fields.Char(string="Code", help="Write the code or operations the calculation must take into account",
                       compute="get_code", inverse="_pass", store=True)
    need_id = fields.Many2one('nutrimental.needs', string="Nutrimental need",
                              help="Used to specify the need that is needed to cover")
    reference_value = fields.Float(string="Reference value")
    uom_id = fields.Many2one('uom.uom', string="Unit of measure", compute="get_default_uom", inverse="_pass",
                             store=True)

    @api.depends('nutriment_ids')
    def get_default_uom(self):
        for record in self:
            if len(record.nutriment_ids.mapped('uom_id')) == 1:
                record.uom_id = record.nutriment_ids[0].uom_id.id
            else:
                record.uom_id = False

    def _pass(self):
        pass

    @api.depends('nutriment_ids', 'nutriment_ids.code')
    def get_code(self):
        for record in self:
            if len(record.nutriment_ids) == 1 and len(record.nutriment_ids.code) == 1:
                record.code = record.nutriment_ids[0].name
            else:
                record.code = False
