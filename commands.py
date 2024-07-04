#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import decimal

import pandas as pd

# Records to represent the objects of this problem.
class Vpp:
    def __init__(self, name, revenue_percentage, daily_fee):        
        self.name = name
        self.revenue_percentage = float(revenue_percentage)
        self.daily_fee = decimal.Decimal(daily_fee)

    def __str__(self):
        return f"VPP name: {self.name}, percent: {self.revenue_percentage}, fee: {self.daily_fee}"
    
    def __repr__(self):
        return self.__str__()

class Site:
    def __init__(self, vpp_name, nmi, address):
        self.vpp_name = vpp_name
        self.nmi = nmi.lower()
        self.address = address

    def __str__(self):
        return f"Site VPP: {self.vpp_name}, nmi: {self.nmi}, address: {self.address}"

    def __repr__(self):
        return self.__str__()

class Battery:
    def __init__(self, nmi, manufacturer, serial_num, capacity):
        self.nmi = nmi.lower()
        self.manufacturer = manufacturer
        self.serial_num = serial_num
        self.capacity = float(capacity)

    def __str__(self):
        return (f"Battery nmi: {self.nmi}, "
                f"manufacturer: {self.manufacturer}, "
                f"serial_num: {self.serial_num}, "
                f"capacity: {self.capacity}")

    def __repr__(self):
        return self.__str__()

# Objects stored in lists below.
VPPS = []
SITES = []
BATTERIES = []

"""
A rule returns a tuple (bool, message). Pass/fail and
error message for the failed rule.
"""

def vpp_percentage_is_sensible(vpp):
    """
    Confirms VPP revenue share between 0% and 100%.
    """
    percent_too_low = vpp.revenue_percentage < 0.0
    percent_too_high = vpp.revenue_percentage > 1.0
    if percent_too_low or percent_too_high:
        return (False, f"VPP revenue percentage not sensible: {vpp.revenue_percentage}")
    else:
        return (True, "")

VPP_RULES = [vpp_percentage_is_sensible]
SITE_RULES = []
BATTERY_RULES = []


def _append_new_object(obj, collection, rules):
    """
    Verify and add a new record to our collection.
    """
    # Execute rules to check object.
    results = [rule(obj) for rule in rules]
    failures = list(filter(lambda x: x[0] == False, results))
    # Exception if there were problems creating a VPP.
    is_failed_results = len(failures) > 0
    if is_failed_results:
        # Combine failed results into error message.
        failure_messages = [failure[1] for failure in failures]
        messages = "\n".join(failure_messages)
        raise Exception(f"Problem(s) found creating new VPP: {obj}\n\n"
                        f"Rule violations:"
                        f"\n{messages}")
    else:
        # Append good VPP to our collection.
        collection.append(obj)

# Error checking happens in the create functions.
def create_vpp(name, revenue_percentage, daily_fee):
    next_vpp = Vpp(name, revenue_percentage, daily_fee)
    _append_new_object(next_vpp, VPPS, VPP_RULES)
        
def create_site(vpp_name, nmi, address):
    next_site = Site(vpp_name, nmi, address)
    _append_new_object(next_site, SITES, SITE_RULES)
    
def create_battery(nmi, manufacturer, serial_num, capacity):
    next_battery = Battery(nmi, manufacturer, serial_num, capacity)
    _append_new_object(next_battery, BATTERIES, BATTERY_RULES)
    
def import_events(filename):
    df = pd.read_csv(filename)

def _populate_objects(filename):
    df = pd.read_csv(filename, dtype={
        "revenue_percentage": "string",
        "daily_fee": "string",
        "serial_num": "string",
        "capacity": "string"
    })
    # Populate each object, use "type" column to dispach
    for _, row in df.iterrows():
        type_name = row["type"]
        if type_name == "vpp":
            create_vpp(name=row["name"],
                       revenue_percentage=row["revenue_percentage"],
                       daily_fee=row["daily_fee"])
        elif type_name == "site":
            create_site(vpp_name=row["vpp_name"],
                        nmi=row["nmi"],
                        address=row["address"])
        elif type_name == "battery":
            create_battery(nmi=row["nmi"],
                           manufacturer=row["manufacturer"],
                           serial_num=row["serial_num"],
                           capacity=row["capacity"])
        else:
            raise Exception(f"Unknown object type encountered during setup:\n {row}")
    
def create_report(vpp_name, year_month):
    # The VPP gets its daily rate first.

    # The VPP gets its first slice according to its own percentage value.

    # Each site gets 80% directly.

    # Each site gets the remaining amount by proportion of its battery.
    pass

if __name__ == "__main__":
    _populate_objects("test_objects.csv")
    for obj in VPPS + SITES + BATTERIES:
        print(obj)
