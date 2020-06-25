import pandas as pd
import logging

from halalmas.server.orders.happy_hour.models import (
    OrderHappyHourGroup, OrderHappyHour
)

OrderStatus = OrderHappyHourGroup.OrderStatus 

class HappyHourOrderStatus(object):
    def __init__(self, *args, **kwargs):
        self.today = pd.Timestamp('today')

    def active_to_complete(self):
        print(f'today: {self.today}')
        orders = OrderHappyHourGroup.objects.filter(order_status=OrderStatus.ACTIVE,
            delstatus=False)
        for idx, order in enumerate(orders):
            print(f'[{idx}] {order.order_group_no} {order.use_date}')
            use_date = order.use_date
            time_end = order.time_end or '23:59:59'
            limit_date = pd.Timestamp(f'{use_date} {time_end}')
            if self.today > limit_date and order.payment_method != OrderHappyHourGroup.PaymentMethod.ON_THE_SPOT:
                print(f'{order.order_group_no} #1=> {limit_date} => change to complete')
                order.order_status = OrderStatus.COMPLETE
                order.save()
            elif self.today > limit_date and \
                order.payment_method == OrderHappyHourGroup.PaymentMethod.ON_THE_SPOT and \
                order.is_redeem==True:
                print(f'{order.order_group_no} #2=> {limit_date} => change to complete')
                order.order_status = OrderStatus.COMPLETE
                order.save()
            else: 
                print('no one can change to complete')
        
    def pending_to_expired(self):
        print(f'today: {self.today}')
        orders = OrderHappyHourGroup.objects.filter(order_status=OrderStatus.PENDING,
            delstatus=False)

        for idx, order in enumerate(orders):
            print(f'[{idx}] {order.order_group_no} {order.use_date}')
            use_date = order.use_date
            time_start = order.time_start or '23:59:59'
            limit_date = pd.Timestamp(f'{use_date} {time_start}')
            if self.today > limit_date:
                print(f'{order.order_group_no} => {limit_date} => change to expired')
                order.order_status = OrderStatus.EXPIRED
                order.save()
            else: 
                print('no one can change to expired')
                
    def active_to_expired(self):
        print(f'today: {self.today}')
        orders = OrderHappyHourGroup.objects.filter(order_status=OrderStatus.ACTIVE,
            is_redeem=False, payment_method = OrderHappyHourGroup.PaymentMethod.ON_THE_SPOT,
            delstatus=False)

        for idx, order in enumerate(orders):
            print(f'[{idx}] {order.order_group_no} {order.use_date}')
            use_date = order.use_date
            time_start = order.time_start or '23:59:59'
            limit_date = pd.Timestamp(f'{use_date} {time_start}')
            if self.today > limit_date:
                print(f'{order.order_group_no} => {limit_date} => change to expired')
                order.order_status = OrderStatus.EXPIRED
                order.save()
            else: 
                print('no one can change to expired')