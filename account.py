from openerp import models, api, fields

class res_partner(models.Model):
	_inherit = "res.partner"

	first_unpaid_invoice = fields.Date('Fecha Factura',help='Fecha de la primera factura impaga',compute='compute_first_unpaid_invoice')

	@api.one
	def compute_first_unpaid_invoice(self):
		first_invoice = self.env['account.invoice'].search([('state','=','open'),('partner_id','=',self.id)],\
			order='id asc',limit=1)
		if first_invoice:
			self.first_unpaid_invoice = first_invoice.date_invoice
		else:
        		self.first_unpaid_invoice = None
