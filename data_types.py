# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

class HL7DataType(object):
    """ generic HL7 data type """
    component_map = None

    def __init__(self, composite, delimiters):
        self.delimiters = delimiters
        self.sub_composites = composite.split(delimiters.subcomposite)

        if self.component_map:
            for index, value in enumerate(self.sub_composites):
                setattr(self, self.component_map[index], value)

    def __str__(self):
        return self.delimiters.subcomposite.join(self.sub_composites)
        
    def __unicode__(self):
        return self.delimiters.subcomposite.join(self.sub_composites)
        

class HL7_ExtendedPersonName(HL7DataType):
    """
        extended person name
        example input:
            EVERYMAN^ADAM^A^III
    """
    component_map = [
        'family_name',
        'given_name',
        'middle_name',
        'suffix',
        'prefix',
        'degree',
        'name_type_code',
    ]


class HL7_SI(HL7DataType):
    component_map = [ 'sequence_id', ]

class HL7_ExtendedCompositeId(HL7DataType):
    """ extended composite id with check digit """

    component_map = [
        'id_number',
        'identifier_check_digit',
        'check_digit_scheme',
        'assigning_authority',
        'identifier_type_code',
        'assigning_facility',
        'effective_date',
        'expiration_date',
        'assigning_jurisdiction',
        'assigning_agency_or_department',
        'security_check',
        'security_check_scheme',
    ]

class HL7Datetime(HL7DataType):
    """
        example input:
            198808181126
    """
    component_map = [ 'datetime' ]

    def __init__(self, composite, delimiter):
        precision = len(composite)
        year = int(composite[0:4])

        if precision >= 6: month = int(composite[4:6])
        else: month = 1

        if precision >= 8: day = int(composite[6:8])
        else: day = 1

        if precision >= 10: hour = int(composite[8:10])
        else: hour = 0

        if precision >= 12: minute = int(composite[10:12])
        else: minute = 0

        if precision >= 14: second = int(composite[12:14])
        else: second = 0

        if precision >= 16: tenth_second = int(composite[14:16])
        else: tenth_second = 0

        if precision >= 19: microsecond = int(composite[16:19]) * 100
        else: microsecond = 0

        if precision == 24: timezone = composite[19:24]
        else: timezone = None

        # TODO: consider timezone
        self.datetime = datetime(year, month, day, hour, minute, second, microsecond)

    def isoformat(self):
        return self.datetime.isoformat()


    def __str__(self):
        return self.datetime.strftime('%Y%m%d%H%M%S')

    def __unicode__(self):
        return self.__str__()


class HL7_CWE(HL7DataType):
    pass

class HL7_XAD(HL7DataType):
    pass

class HL7_ExtendedTelecommunicationNumber(HL7DataType):
    """ XTN - extended telecommunication number """
    pass

class HL7_ST(HL7DataType):
    pass

class HL7_ID(HL7DataType):
    pass

class HL7_NM(HL7DataType):
    pass

class HL7_HD(HL7DataType):
    pass


data_types = {
    "ST": "String Data",
    "TX": "Text Data",
    "SI": "Sequence ID",
    "IS": "Coded Value For User-defined Tables",
    "ID": "Coded Values For Hl7 Tables",
    "FT": "Formatted Text Data",
    "TM": "Time",
    "DT": "Date",
    "DTM": "Date/Time",
    "NM": "Numeric",
    "varies": "None",
    "AD": "Address",
    "AUI": "Authorization Information",
    "CCD": "Charge Code and Date",
    "CCP": "Channel Calibration Parameters",
    "CD": "Channel Definition",
    "CE": "Coded Element",
    "CF": "Coded Element with Formatted Values",
    "CNE": "Coded with No Exceptions",
    "CNN": "Composite ID Number and Name Simplified",
    "CP": "Composite Price",
    "CQ": "Composite Quantity with Units",
    "CSU": "Channel Sensitivity and Units",
    "CWE": "Coded with Exceptions",
    "CX": "Extended Composite ID with Check Digit",
    "DDI": "Daily Deductible Information",
    "DIN": "Date and Institution Name",
    "DLD": "Discharge to Location and Date",
    "DLN": "Driver's License Number",
    "DLT": "Delta",
    "DR": "Date/Time Range",
    "DTN": "Day Type and Number",
    "ED": "Encapsulated Data",
    "EI": "Entity Identifier",
    "EIP": "Entity Identifier Pair",
    "ELD": "Error Location and Description",
    "ERL": "Error Location",
    "FC": "Financial Class",
    "FN": "Family Name",
    "GTS": "General Timing Specification",
    "HD": "Hierarchic Designator",
    "ICD": "Insurance Certification Definition",
    "JCC": "Job Code/Class",
    "LA1": "Location with Address Variation 1",
    "LA2": "Location with Address Variation 2",
    "MA": "Multiplexed Array",
    "MO": "Money",
    "MOC": "Money and Code",
    "MOP": "Money or Percentage",
    "MSG": "Message Type",
    "NA": "Numeric Array",
    "NDL": "Name with Date and Location",
    "NR": "Numeric Range",
    "OCD": "Occurrence Code and Date",
    "OSD": "Order Sequence Definition",
    "OSP": "Occurrence Span Code and Date",
    "PIP": "Practitioner Institutional Privileges",
    "PL": "Person Location",
    "PLN": "Practitioner License or Other ID Number",
    "PPN": "Performing Person Time Stamp",
    "PRL": "Parent Result Link",
    "PT": "Processing Type",
    "PTA": "Policy Type and Amount",
    "QIP": "Query Input Parameter List",
    "QSC": "Query Selection Criteria",
    "RCD": "Row Column Definition",
    "RFR": "Reference Range",
    "RI": "Repeat Interval",
    "RMC": "Room Coverage",
    "RP": "Reference Pointer",
    "RPT": "Repeat Pattern",
    "SAD": "Street Address",
    "SCV": "Scheduling Class Value Pair",
    "SN": "Structured Numeric",
    "SPD": "Specialty Description",
    "SPS": "Specimen Source",
    "SRT": "Sort Order",
    "TQ": "Timing Quantity",
    "TS": "Time Stamp",
    "UVC": "UB Value Code and Amount",
    "VH": "Visiting Hours",
    "VID": "Version Identifier",
    "VR": "Value Range",
    "WVI": "Channel Identifier",
    "WVS": "Waveform Source",
    "XAD": "Extended Address",
    "XCN": "Extended Composite ID Number and Name for Persons",
    "XON": "Extended Composite Name and Identification Number for Organizations",
    "XPN": "Extended Person Name",
    "XTN": "Extended Telecommunication Number",
}
