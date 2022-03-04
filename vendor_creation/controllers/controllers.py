# -*- coding: utf-8 -*-
# from odoo import http


# class VendorCreation(http.Controller):
#     @http.route('/vendor_creation/vendor_creation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vendor_creation/vendor_creation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vendor_creation.listing', {
#             'root': '/vendor_creation/vendor_creation',
#             'objects': http.request.env['vendor_creation.vendor_creation'].search([]),
#         })

#     @http.route('/vendor_creation/vendor_creation/objects/<model("vendor_creation.vendor_creation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vendor_creation.object', {
#             'object': obj
#         })
