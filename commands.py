#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Records to represent the objects of this problem.
class Vpp:
    def __init__(self, name, revenue_percentage, daily_fee):        
        self.name = name
        self.revenue_percentage = float(revenue_percentage)
        self.daily_fee = int(daily_fee)

    def __str__(self):
        return f"VPP name: {self.name}, %: {self.revenue_percentage}, fee: {self.daily_fee}"

class Site:
    def __init__(self, vpp_name, nmi, address):
        self.vpp_name = vpp_name
        self.nmi = nmi
        self.address = address

    def __str__(self):
        return f"Site VPP: {self.vpp_name}, nmi: {self.nmi}, address: {self.address}"

class Battery:
    def __init__(self, nmi, manufacturer, serial_num, capacity):
        self.nmi = nmi
        self.manufacturer = manufacturer,
        self.serial_num = serial_num
        self.capacity = float(capacity)

    def __str__(self):
        return (f"Battery nmi: {self.nmi}, "
                f"manufacturer: {self.manufacturer}, "
                f"serial_num: {self.serial_num}, "
                f"capacity: {self.capacity}")

# Objects stored in lists below.
VPPS = []
SITES = []
BATTERIES = []

# Error checking happens in the create functions.
def create_vpp(name, revenue_percentage, daily_fee):
    pass
def create_site(vpp_name, nmi, address):
    pass
def create_battery(nmi, manufacturer, serial_num, capacity):
    pass
def import_events(filename):
    pass
def create_report(vpp_name, year_month):
    pass
