# See LICENSE file for full copyright and licensing details.


from odoo import api, models,fields, _
from odoo.exceptions import UserError


class sale_order(models.Model):
    _inherit = "sale.order"

    def check_limits(self):
        self.ensure_one()

        partner = self.partner_id
        user_id = self.env['res.users'].search([
            ('partner_id', '=', partner.id)], limit=1)
        if partner.is_weak_credit_history and user_id.credit_limit != partner.credit_limit:
            if user_id and not user_id.has_group('base.group_portal') or not \
                    user_id:
                moveline_obj = self.env['account.move.line']
                movelines = moveline_obj.search(
                    [('partner_id', '=', partner.id),
                     ('account_id.user_type_id.name', 'in',
                      ['Receivable', 'Payable'])]
                )
                confirm_sale_order = self.search([('partner_id', '=', partner.id),
                                                  ('state', '=', 'sale')])
                debit, credit = 0.0, 0.0
                amount_total = 0.0
                for status in confirm_sale_order:
                    amount_total += status.amount_total
                for line in movelines:
                    credit += line.credit
                    debit += line.debit
                partner_credit_limit = (partner.credit_limit - debit) + credit
                available_credit_limit = \
                    (partner_credit_limit - debit)
                if (amount_total - debit) > available_credit_limit:
                    if not partner.over_credit:
                        msg = 'Your available credit limit' \
                              ' Amount = %s \nCheck "%s" Accounts or Credit ' \
                              'Limits.' % (partner.credit_limit,
                                           self.partner_id.name)
                        raise UserError(_('You can not confirm Sale '
                                          'Order. \n' + msg))
                    # partner.write(
                    #     {'credit_limit': credit - debit + self.amount_total})
                return True
        else:
            partners = self.env.user
            user_id = self.search([
                ('user_id', '=', partners.id)], limit=1)
            if partners and not partners.has_group('base.group_portal') or not \
                    partners:
                moveline_obj = self.env['account.move.line']
                movelines = moveline_obj.search(
                    [
                      ('move_id.invoice_user_id', '=', partners.id),
                      ('account_id.user_type_id.name', 'in',
                      ['Receivable', 'Payable'])]
                )
                moveline_obj = self.env['account.move']
                confirm_sale_order = moveline_obj.search([('invoice_user_id', '=', partners.id),
                                                  ('state', '=', 'draft')])
                debit, credit = 0.0, 0.0
                amount_total = 0.0
                for status in confirm_sale_order:
                    amount_total += status.amount_total
                for line in movelines:
                    credit += line.credit
                    debit += line.debit
                partners_credit_limit = (partners.credit_limit - debit) + credit
                available_credit_limit = \
                    (partners_credit_limit - debit)
                if (amount_total - debit) > available_credit_limit:
                    msg = 'Your available credit limit' \
                          ' Amount = %s \nCheck "%s" Accounts or Credit ' \
                          'Limits.' % (partners.credit_limit,
                                       self.user_id.name)
                    raise UserError(_('You can not confirm Sale '
                                          'Order. \n' + msg))
                return True

    def action_confirm(self):
        res = super(sale_order, self).action_confirm()
        for order in self:
            order.check_limits()
        return res

    # @api.constrains('amount_total')
    # def check_amounts(self):
    #     for order in self:
    #         order.check_limits()