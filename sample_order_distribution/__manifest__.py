{
    'name': 'Sample Order Distribution',
    'version': '17.0.0.1',
    'sequence': -500,
    'summary': 'Module for managing sample order distributions',
    'description': 'This module helps in managing the distribution of sample orders.',
    'author': '',
    'depends': ['base','sale', 'stock', 'crm'],
    'data': ['security\ir.model.access.csv',
             'view\sample_order.xml',
             'view\sample_products.xml',
             'view\sample_location.xml',
             'view/autovalidate_wizard.xml',
             # 'view\crm_lead_view.xml'
             ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
