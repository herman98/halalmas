import pandas as pd
import logging
from django.db.models import Count

from halalmas.server.hosts.branches.models import (
    Branch
)
from halalmas.server.hosts.happy_hour.models import BranchHappyHourSlotHeader

class BranchHappyHourStatus(object):
    def __init__(self, *args, **kwargs):
        self.today = pd.Timestamp('today')

    def happyhour_disable_status(self):
        print(f'today: {self.today}')
        #check slot header with expired from today 
        # hh_header = BranchHappyHourSlotHeader.objects.values('branch') \
        #     .annotate(cnt_branch=Count('branch')) \
        #     .filter(date_end__lte=self.today.date(), delstatus=False, cnt_branch__gte=1) \
        #     .order_by('branch')
        hh_header = BranchHappyHourSlotHeader.objects \
            .filter(date_end__lte=self.today.date(), delstatus=False) \
            .order_by('branch')
        print(f'hh_header count {hh_header.count()}')
        for idx, item in enumerate(hh_header):
            print(f'[{idx}] branch:{item.branch} pk:{item.pk}')
            
            check_other_header_exist = BranchHappyHourSlotHeader.objects \
                .filter(branch=item.branch, date_end__gte=self.today.date()) \
                .count() 
            if check_other_header_exist >= 1:
                continue

            branch_update = item.branch
            if branch_update.is_happy_hour == True:
                branch_update.is_happy_hour = False
                branch_update.save()
                print(f'branch id={branch_update.id} updated')
            else:
                print(f'branch id={branch_update.id} is false')
        
        #update status header to true
        # if hh_header.count() > 0:
        #     hh_header.update(delstatus=True)
        #     print(f'hh_header update delstatus to TRUE success')            
                
