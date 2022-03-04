# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = 'res.users'


class Partner(models.Model):
    _inherit = 'res.partner'


    @api.model
    def default_get(self, fields_list):
        res = super(Partner, self).default_get(fields_list)
        user_id = self.env.user
        if user_id:
            res['user_id'] = user_id.id
            res['credit_limit'] = user_id.credit_limit
        return res