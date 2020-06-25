import pandas
import calendar

from django.conf import settings

from halalmas.server.configuration.models import CalendarDimension, CalendarDate


START_DATE = "{}/1/{}"
END_DATE = "{}/{}/{}"


class GenerateCalendarDate(object):
    def __init__(self, year_selected=None):
        self.year_selected = year_selected

    def generate(self):
        if self.year_selected:
             # means all records
            print("START Generate Calender Date")
            # generate dimension table
            for here_month in range(1, 13):
                print("month: {}".format(here_month))

                obj_dimension, created = CalendarDimension.objects.update_or_create(
                    year=self.year_selected, month=here_month,
                    defaults={'year': self.year_selected,
                              'month': here_month},
                )
                max_day = calendar.monthrange(self.year_selected, here_month)
                # generate date
                start_date = START_DATE.format(here_month, self.year_selected)
                end_date = END_DATE.format(
                    here_month, max_day[1], self.year_selected)
                aa = pandas.date_range(start=start_date, end=end_date)
                for date_item in aa.date:
                    print("date_item: {}".format(date_item))
                    if date_item.weekday() < 5:
                        obj, created = CalendarDate.objects.update_or_create(
                            dimension=obj_dimension,
                            calendar_date=date_item,
                            defaults={'dimension': obj_dimension,
                                      'calendar_date': date_item,
                                      'status': CalendarDate.CalendarDateType.WEEKDAY},
                        )
                    else:
                        obj, created = CalendarDate.objects.update_or_create(
                            dimension=obj_dimension,
                            calendar_date=date_item,
                            defaults={'dimension': obj_dimension,
                                      'calendar_date': date_item,
                                      'status': CalendarDate.CalendarDateType.WEEKEND},
                        )

            print("DONE Generate Calender Date")

        else:
            # means with limit
            print("CAN NOT PROCEED year_selected {} seletected.".format(
                self.year_selected))
