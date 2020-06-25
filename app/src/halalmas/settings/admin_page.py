ADMIN_REORDER = (
    # 'sites',
    # Reorder app models
    {'app': 'objects', 'label': 'Master Data',
        'models': (
            {'model': 'objects.brands', 'label': 'Brand'},
        )
     },

    # Reorder app models
    {'app': 'auth', 'label': 'CRM AUTHENTICATION AND AUTHORIZATION',
        'models': ('auth.User', 'auth.Group',
                   #    {'model': 'crm.CRMSetting', 'label': 'Dashboard'},
                   )
     },

    {'app': 'authtoken', 'label': 'AUTH TOKEN',
        'models': ('authtoken.Token',
                   )
     },

    {'app': 'oauth2_provider', 'label': 'Django OAuth Toolkit',
     'models': (
         'oauth2_provider.AccessToken',
         'oauth2_provider.Application',
         'oauth2_provider.Grant',
         'oauth2_provider.RefreshToken',
     )
     },

    {'app': 'social_django', 'label': 'Python Social Auth',
     'models': (
         'social_django.Association',
         'social_django.Nonce',
         'social_django.UserSocialAuth',
     )
     },

    # CELERY PERIODIC TASKS
    {'app': 'django_celery_beat', 'label': 'CELERY PERIODIC TASKS',
     'models': (
         {'model': 'django_celery_beat.CrontabSchedule', 'label': 'Crontabs'},
         {'model': 'django_celery_beat.IntervalSchedule', 'label': 'Intervals'},
         {'model': 'django_celery_beat.PeriodicTask', 'label': 'Periodic tasks'},
         {'model': 'django_celery_beat.SolarSchedule', 'label': 'Solar events'},
         #  'django_celery_beat.PeriodicTasks',
     )
     },

    # CELERY RESULTS
    {'app': 'django_celery_results', 'label': 'CELERY RESULTS',
     'models': (
         'django_celery_results.TaskResult',
     )
     },
)
