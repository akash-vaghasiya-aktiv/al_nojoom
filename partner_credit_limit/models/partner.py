# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    over_credit = fields.Boolean('Allow Over Credit?')
    is_weak_credit_history = fields.Boolean('Is Weak Credit History?')
    # credit_limit = fields.Float(related='credit_limit')
    credit_limit_related = fields.Float(related='credit_limit', string="Display Credit Limit")

    @api.onchange('is_weak_credit_history')
    def onchange_spouse(self):
        if self.is_weak_credit_history == False:
            if self.user_id and self.user_id.credit_limit:
                self.write({
                        'credit_limit' : self.user_id.credit_limit
                    })

    def write(self, vals):
        if vals and vals.get('is_weak_credit_history') == False:
            if self.user_id and self.user_id.credit_limit:
                vals['credit_limit'] = self.user_id.credit_limit
        if vals and vals.get('user_id'):
            user_id = self.env['res.users'].browse(vals.get('user_id'))
            if user_id:
                vals['credit_limit'] = user_id.credit_limit
        return super(ResPartner, self).write(vals)

