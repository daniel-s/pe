#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import decimal
import json

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

# Lookup VPP by identifier.
def _2get_vpp_by_name(name):
    for vpp in VPPS:
        if vpp.name == name:
            return vpp
    raise Exception(f"VPP with name {name} could not be found.")

def _2get_site_by_nmi(nmi):
    for site in SITES:
        if site.nmi == nmi:
            return site
    raise Exception(f"Site with nmi {nmi} could not be found.")

def _get_events_df():
    """
    Compiles the df on the fly. Can be replaced by a different,
    more efficient implementation later.
    """
    df = pd.read_csv("test_events.csv")
    # Keep all nmis lower case
    df["nmi"] = df["nmi"].str.lower()
    return df

def _populate_vpp_to_events(df):
    # Populate the vpp information for later analysis.
    def add_site(row):
        site = _2get_site_by_nmi(row["nmi"])
        row["vpp"] = site.vpp_name
        return row
    df = df.apply(add_site, axis=1)
    return df

def _get_battery_df():
    # Convert to dataframe
    batteries = []
    for battery in BATTERIES:
        new_battery = {
            "nmi": battery.nmi,
            "capacity": battery.capacity,
            "vpp": _2get_site_by_nmi(battery.nmi).vpp_name
        }
        batteries.append(new_battery)

    df = pd.DataFrame(batteries)
    return df
        
def create_report(vpp_name, year_month):
    """
    In practice each block would probably be a separate function
    that could be individually tested. Important as it's the main
    rule engine to allocate funds.
    
    Assume that year_month is of the format "YYYY-MM".
    """
    vpp = _2get_vpp_by_name(vpp_name)
    
    # Data generated from the df of events.
    df = _get_events_df()
    df = _populate_vpp_to_events(df)

    # Filter for the vpp and month requested.
    date_filter = df["date"].str.startswith(year_month)
    name_filter = df["vpp"] == vpp_name
    df = df[date_filter & name_filter]

    # VPP daily fees
    vpp_daily_fee = vpp.daily_fee * 28 # Assumed 28 day month.

    # VPP proportion of fees
    df["fees"] = df["energy"] * df["tarif"]
    df["fee_to_vpp"] = df["fees"] * vpp.revenue_percentage

    # Each site gets 80% directly.
    df["fee_direct_to_site"] = (df["fees"] - df["fee_to_vpp"]) * .8
    site_direct_fees = dict(df.groupby("nmi")["fee_direct_to_site"].sum())
        
    # Apportion remaining 20% to each site in proportion to their batteries.
    # Total to share
    df["fee_to_share"] = df["fees"] - df["fee_to_vpp"] - df["fee_direct_to_site"]
    total_fee_to_share = df["fee_to_share"].sum()
    # Assigning proportions from battery capacity.
    df_bat = _get_battery_df()
    df_bat = df_bat[df_bat["vpp"] == vpp_name]
    total_capacity = df_bat["capacity"].sum()
    df_nmi_proportion = df_bat.groupby("nmi")["capacity"].sum() / total_capacity
    site_proportional_fees = dict(df_nmi_proportion * total_fee_to_share)

    # Collect site results.
    site_results = []
    sites_for_vpp = set(df_bat["nmi"]) # Assumes each site has at least 1 battery.
    for site in sites_for_vpp:
        result = {
            "nmi": site
        }
        # Direct fees. 0 if no fees were collected.
        if site in site_direct_fees:
            result["direct_fees"] = f"{round(site_direct_fees[site], 4)}"
        else:
            result["direct_fees"] = "0"
        # The 20% shared fees
        if site in site_proportional_fees:
            result["shared_fees"] = f"{round(site_proportional_fees[site], 4)}"
        else:
            result["shared_fees"] = "0"

        site_results.append(result)
            
    # Compile the results into a report.
    results = {
        "name": vpp_name,
        "daily_fee_for_month": f"{round(vpp_daily_fee, 4)}",
        "sites": site_results
    }
    return results

if __name__ == "__main__":
    _populate_objects("test_objects.csv")
    report_results = create_report("Bellossom", "2022-10")
    print(json.dumps(report_results, indent=4))
