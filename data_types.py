# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

def make_cell_type(name, options=None):
    default_options = {
        'required': False,
        'repeats': False,
        'type': HL7DataType
    }
    if options is None:
        options = {}

    default_options.update(options)
    return (name, default_options)


class HL7DataType(object):
    """ generic HL7 data type """
    field_map = None

    def __init__(self, composite, delimiters, use_delimiter="component_separator"):
        self.delimiters = delimiters
        # delimiter to use
        self.delimiter = getattr(self.delimiters, use_delimiter)

        self.input_fields = composite.split(self.delimiter)

        if self.field_map:
            self.set_attributes(self.field_map, self.input_fields)
        else:
            # if no field_map is given, treat this as a generic data type
            if not self.delimiter in composite:
                self.value = composite
            else:
                for index, value in enumerate(self.input_fields):
                    self.input_fields[index] = HL7DataType(value, delimiters,
                                                    use_delimiter="subcomponent_separator")

    def __str__(self):
        return self.__unicode__()
        
    def __unicode__(self):#
        """ converts the datatype into a unicode string """
        if not self.field_map:
            """ if value is defined, this is just a simple string data type """
            if hasattr(self, "value"):
                return self.value
            else:
                return self.delimiter.join([x.__unicode__() for x in self.input_fields])
        else:
            attrs = []
            # collect all attributes which are defined
            for attr in self.field_map:
                if hasattr(self, attr):
                    attrs.append(getattr(self, attr))
                else:
                    break
            return self.delimiters.component_separator.join(attrs)

        return self.delimiters.component_separator.join(self.sub_composites)

    def set_attributes(self, field_definitions, field_input):
        """
            sets the data in field_input to instance attributes
            as defined in field_definitions
        """
        for index, value in enumerate(field_input):
            name = field_definitions[index][0]
            DataType = field_definitions[index][1]["type"]

            setattr(self, name, DataType(value, self.delimiters,
                                         use_delimiter="subcomponent_separator"))

    def __repr__(self):
        return "< %s >" % self.__unicode__()

    def __getitem__(self, idx):
        return self.input_fields[idx]

class HL7RepeatingField(object):
    """ generic repeating field """
    def __init__(self, Type, composite, delimiters):
        
        # split input data by repetition character
        split_data = composite.split(delimiters.rep_separator)

        self.list_ = [Type(x, delimiters) for x in split_data]

    def __len__(self):
        return len(self.list_)

    def __getitem__(self, idx):
        return self.list_[idx]


class HL7_ExtendedPersonName(HL7DataType):
    """
        extended person name
        example input:
            EVERYMAN^ADAM^A^III
    """
    field_map = [
        make_cell_type('family_name', options = {"required": True}),
        make_cell_type('given_name'),
        make_cell_type('middle_name'),
        make_cell_type('suffix'),
        make_cell_type('prefix'),
        make_cell_type('degree'),
        make_cell_type('name_type_code'),
        make_cell_type('name_representation_code'),
        make_cell_type('name_contact')
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


class HL7_SI(HL7DataType):
    component_map = [ 'sequence_id', ]

class HL7_ExtendedCompositeId(HL7DataType):
    """ extended composite id with check digit """

    field_map = [
        make_cell_type('id_number', options = {"reqired": True}),
        make_cell_type('identifier_check_digit'),
        make_cell_type('check_digit_scheme'),
        make_cell_type('assigning_authority'),
        make_cell_type('identifier_type_code', options = {"required": True}),
        make_cell_type('assigning_facility'),
        make_cell_type('effective_date', options = {"type": HL7Datetime}),
        make_cell_type('expiration_date', options = {"type": HL7Datetime}),
        make_cell_type('assigning_jurisdiction'),
        make_cell_type('assigning_agency_or_department'),
        make_cell_type('security_check'),
        make_cell_type('security_check_scheme')
    ]

class HL7_CWE(HL7DataType):
    pass

class HL7_StreetAddress(HL7DataType):
    """ SAD street address """

    field_map = [
        make_cell_type('street_or_mailing_address'),
        make_cell_type('street_name'),
        make_cell_type('dwelling_number')
    ]

class HL7_ExtendedAddress(HL7DataType):
    """ XAD extended Adress """

    field_map = [
        make_cell_type('street_address', options = {"type": HL7_StreetAddress}),
        make_cell_type('other_designation'),
        make_cell_type('city'),
        make_cell_type('state_or_province'),
        make_cell_type('zip_or_postal_code'),
        make_cell_type('country'),
        make_cell_type('address_type'),
        make_cell_type('other_geographic_designation'),
        make_cell_type('country_code'),
        make_cell_type('census_tract'),
        make_cell_type('address_representation_code'),
        make_cell_type('effective_date', options = {"type": HL7Datetime}),
        make_cell_type('expiration_date', options = {"type": HL7Datetime}),
        make_cell_type('expiration_reason'),
        make_cell_type('bad_address_indicator'),
        make_cell_type('address_usage'),
        make_cell_type('addressee'),
        make_cell_type('comment'),
        make_cell_type('preference_order'),
        make_cell_type('protection_code'),
        make_cell_type('address_identifier')
    ]

class HL7_ExtendedTelecommunicationNumber(HL7DataType):
    """ XTN - extended telecommunication number """
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
