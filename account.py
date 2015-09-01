from openerp import models, api, fields
from datetime import datetime

class res_partner(models.Model):
	_inherit = "res.partner"

	first_unpaid_invoice = fields.Date('Fecha Factura',help='Fecha de la primera factura impaga',compute='compute_first_unpaid_invoice')
	last_sale_date = fields.Date('Fecha Ultimo Pedido',help='Fecha del ultimo pedido del cliente',compute='compute_last_sale_order')
	avg_sales_amount = fields.Float('Monto Promedio',help='Monto Promedio de los Pedidos',compute='compute_avg_sales_amount')
	sales_frequency = fields.Integer('Frecuencia de Ventas',help='Frecuencia (en dias) en los cuales el cliente realiza su pedido',compute='compute_sales_frequency')

	@api.one
	def compute_first_unpaid_invoice(self):
		first_invoice = self.env['account.invoice'].search([('state','=','open'),('partner_id','=',self.id)],\
			order='id asc',limit=1)
		if first_invoice:
			self.first_unpaid_invoice = first_invoice.date_invoice
		else:
        		self.first_unpaid_invoice = None

	@api.one
	def compute_last_sale_order(self):
		last_sale_order = self.env['sale.order'].search([('state','not in',['draft','sent','cancel']),('partner_id','=',self.id)],\
			order='id desc',limit=1)
		if last_sale_order:
			self.last_sale_date = last_sale_order.date_order
		else:
			self.last_sale_date = None

	@api.one
	def compute_avg_sales_amount(self):
		sale_orders = self.env['sale.order'].search([('state','not in',['draft','sent','cancel']),('partner_id','=',self.id)])
		index = 0.00
		amount = 0
		for sale_order in sale_orders:
			amount += sale_order.amount_untaxed
			index += 1
		if index > 0:
			self.avg_sales_amount = amount / index
		else:
			self.avg_sales_amount = 0.00

	@api.one
	def compute_sales_frequency(self):
		sale_orders = self.env['sale.order'].search([('state','not in',['draft','sent','cancel']),('partner_id','=',self.id)],order='id asc')
		index = 0.00
		days = 0
		last_date_order = None
		for sale_order in sale_orders:
			if not last_date_order:
				last_date_order = sale_order.date_order
			else:
				date_object = datetime.strptime(sale_order.date_order,'%Y-%m-%d %H:%M:%S')
				last_date_object = datetime.strptime(last_date_order,'%Y-%m-%d %H:%M:%S')
				days = days + (date_object - last_date_object).days	
			index += 1
		if index > 0:
			self.sales_frequency = days / index
		else:
			self.sales_frequency = 0.00
