# """
# halalmas-crm DB Router
# """


# class CRMDBRouter(object):

#     def db_for_read(self, model, **hints):
#         "Point all operations on chinook models to 'tempatcrm_db'"
#         # print(f'model._meta.app_label {model._meta.app_label}')
#         if model._meta.app_label == 'crm':
#             return 'tempatcrm_db'
#         return 'default'

#     def db_for_write(self, model, **hints):
#         "Point all operations on xwork models to 'tempatcrm_db'"
#         # print(f'model._meta.app_label {model._meta.app_label}')
#         if model._meta.app_label == 'crm':
#             return 'tempatcrm_db'
#         return 'default'

#     def allow_relation(self, obj1, obj2, **hints):
#         "Allow any relation if a both models in crm app"
#         # print(f'obj1._meta.app_label {obj1._meta.app_label}')
#         if obj1._meta.app_label == 'crm' and obj2._meta.app_label == 'crm':
#             return True
#         elif 'crm' not in [obj1._meta.app_label, obj2._meta.app_label]:
#             return True
#         return False

#     def allow_syncdb(self, db, model):
#         # print(f'model._meta.app_label {model._meta.app_label}')
#         if db == 'tempatcrm_db' or model._meta.app_label == "crm":
#             return True
#         return False

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Make sure the auth app only appears in the 'tempatcrm_db'
#         database.
#         """
#         # print(f'model._meta.app_label {app_label}')
#         if app_label == 'crm':
#             return db == 'tempatcrm_db'
#         return 'default'
