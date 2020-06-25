from abc import ABCMeta, abstractproperty, abstractmethod
from typing import List, Dict

from halalmas.core.typing import DateTime

# Interface


class IndonesiaAdministrativeArea():

    @abstractproperty
    def negara(self):
        raise NotImplementedError

    @abstractproperty
    def provinsi(self):
        raise NotImplementedError

    @abstractproperty
    def kabupaten(self):
        raise NotImplementedError

    @abstractproperty
    def kecamatan(self):
        raise NotImplementedError

    @abstractproperty
    def kelurahan(self):
        raise NotImplementedError


class AreaPropertyInfo():

    @abstractproperty
    def has_building(self) -> bool:
        raise NotImplementedError

    @abstractproperty
    def total_building(self) -> int:
        raise NotImplementedError

    @abstractproperty
    def total_meeting_room(self) -> int:
        raise NotImplementedError

    @abstractproperty
    def total_office(self) -> int:
        raise NotImplementedError

    @abstractproperty
    def total_event_space(self) -> int:
        raise NotImplementedError

    @abstractproperty
    def total_virtual_office(self) -> int:
        raise NotImplementedError


class AreaBookingInfo():

    @abstractmethod
    def total_booking(self, date1: DateTime, date2: DateTime) -> int:
        return NotImplementedError

    @abstractmethod
    def total_booking_meeting_hourly(self, date1: DateTime, date2: DateTime) -> int:
        return NotImplementedError

    @abstractmethod
    def total_booking_meeting_package(self, date1: DateTime, date2: DateTime) -> int:
        return NotImplementedError

    @abstractmethod
    def total_booking_office(self, date1: DateTime, date2: DateTime) -> int:
        return NotImplementedError

    @abstractmethod
    def total_booking_event_space(self, date1: DateTime, date2: DateTime) -> int:
        return NotImplementedError

    @abstractmethod
    def total_booking_virtual_office(self, date1: DateTime, date2: DateTime) -> int:
        return NotImplementedError


class AreaStatistic():

    @staticmethod
    def top5_provinsi(self, date1: DateTime, date2: DateTime) -> str:
        return NotImplementedError

    @staticmethod
    def top5_kabupaten(self, date1: DateTime, date2: DateTime) -> str:
        return NotImplementedError

    @staticmethod
    def top5_kecamatan(self, date1: DateTime, date2: DateTime) -> str:
        return NotImplementedError

    @staticmethod
    def top5_kelurahan(self, date1: DateTime, date2: DateTime) -> str:
        return NotImplementedError
