# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from __future__ import absolute_import
from datetime import datetime
from six.moves import map
import six


def make_cell_type(name, options=None, index=None):
    """
    helper method used to configure HL7DataType field maps. Provides some
    sensible default values for HL7 data types.
    """
    default_options = {
        'required': False,
        'repeats': False,
        'type': HL7DataType,
        'index': index,
    }
    if options is None:
        options = {}

    default_options.update(options)
    return (name, default_options)


class HL7DataType(object):
    """ Generic HL7 data type, can be used as field data type or subfield data
    type. You can inherit from this class to define your own data types. Simply
    provide a field_map list to define the possible (sub)fields in this data
    type.

    A field_map entry is provided as a tuple ('field_name', options) with
    options being a dict with entries 'required', 'repeats', 'type'. You can
    use make_cell_type as a helper method to create field_map entries.
    """
    field_map = None

    def __init__(
            self, composite, delimiters, use_delimiter="component_separator"):
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
                    self.input_fields[index] = HL7DataType(
                        value,
                        delimiters,
                        use_delimiter="subcomponent_separator"
                    )

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        """ converts the datatype into a unicode string """

        if not self.field_map:
            """ if value is defined, this is just a simple string data type """
            if hasattr(self, "value"):
                return six.text_type(self.value)
            else:
                return self.delimiter.join(
                    six.text_type(x) for x in self.input_fields)
        else:
            attrs = []
            # collect all attributes which are defined
            for attr, options in self.field_map:
                value = getattr(self, attr)
                if value is not None:
                    attrs.append(value)
                else:
                    break
            return self.delimiter.join(map(six.text_type, attrs))

    def set_attributes(self, field_definitions, field_input):
        """
            sets the data in field_input to instance attributes
            as defined in field_definitions
        """

        input_length = len(field_input)
        for index, definition in enumerate(field_definitions):
            name = definition[0]
            if index < input_length:
                DataType = definition[1]["type"]
                setattr(
                    self, name,
                    DataType(
                        field_input[index],
                        self.delimiters,
                        use_delimiter="subcomponent_separator")
                )
            else:
                setattr(self, name, None)

    def __getitem__(self, idx):
        return self.input_fields[idx]

    def __len__(self):
        return len(self.input_fields)

    def __nonzero__(self):
        if not self.field_map and hasattr(self, "value"):
            return bool(self.value)
        elif len(self.input_fields) == 1:
            return bool(self.input_fields[0])
        elif len(self.input_fields) > 1:
            return True

    def __bool__(self): # pragma: no cover
        return self.__nonzero__()

class HL7RepeatingField(object):
    """ generic repeating field """
    def __init__(self, Type, composite, delimiters):

        self.delimiters = delimiters

        # split input data by repetition character
        split_data = composite.split(delimiters.rep_separator)

        self.list_ = [Type(x, delimiters) for x in split_data]

    def __len__(self):
        return len(self.list_)

    def __getitem__(self, idx):
        return self.list_[idx]

    def __unicode__(self):
        return self.delimiters.rep_separator.join(map(six.text_type, self.list_))

    def __str__(self): # pragma: no cover
        return self.__unicode__()


class HL7_ExtendedPersonName(HL7DataType):
    """
        extended person name
        example input:
            EVERYMAN^ADAM^A^III
    """
    field_map = [
        make_cell_type('family_name', options={"required": True}),
        make_cell_type('given_name'),
        make_cell_type('middle_name'),
        make_cell_type('suffix'),
        make_cell_type('prefix'),
        make_cell_type('degree'),
        make_cell_type('name_type_code'),
        make_cell_type('name_representation_code'),
        make_cell_type('name_context')
    ]


class HL7Datetime(HL7DataType):
    """
        HL7 datetime data type

        Complete Supports the DTM format and only partial support for the older TM format,
        which is deprecated since hl7 2.6.
        If the datetime is given in TM format the second component is ignored, because its not
        reliable and the first component is treated like the DTM formatted datetime.

        example input:
            198808181126
    """
    component_map = ['datetime']

    def __init__(self, composite, delimiters, use_delimiter="component_separator"):

        delimiter = getattr(delimiters, use_delimiter)
        composite = composite.split(delimiter)
        composite = composite[0]

        if len(composite) == 0:
            self.datetime = ""
            self.isNull = True
        else:
            precision = len(composite)
            year = int(composite[0:4])

            if precision >= 6: month = int(composite[4:6])  # noqa
            else: month = 1  #noqa

            if precision >= 8: day = int(composite[6:8])  # noqa
            else: day = 1  #noqa

            if precision >= 10: hour = int(composite[8:10])  #noqa
            else: hour = 0  #noqa

            if precision >= 12: minute = int(composite[10:12])  # noqa
            else: minute = 0  # noqa

            if precision >= 14: second = int(composite[12:14])  # noqa
            else: second = 0  # noqa

            # Skip the "." separator
            if precision >= 17: tenth_second = int(composite[15:17])  # noqa
            else: tenth_second = 0  # noqa

            if precision >= 19:
                microsecond = int(composite[17:19]) * 100
            else: microsecond = 0  #noqa

            if precision == 24: timezone = composite[19:24]  # noqa
            else: timezone = None  #noqa

            # TODO: consider timezone
            try:
                self.datetime = datetime(
                    year, month, day, hour, minute, second, microsecond)
            except ValueError:
                self.datetime = ""
                self.isNull = True
            else:
                self.isNull = False
                self.precision = precision

    def isoformat(self):
        if self.isNull:
            return ""
        else:
            return self.datetime.isoformat()

    def __str__(self):
        if self.isNull:
            return ""
        else:
            # HL7 dates are ISO 8601 without the decorators, i.e.
            # "YYYYMMDDHHMMSS.UUUU[+|-ZZzz]"
            return self.datetime.isoformat(
                str('-')).replace("-", "").replace(":", "")[:self.precision]

    def __unicode__(self):  # pragma: no cover
        return self.__str__()

    def __nonzero__(self):
        return not self.isNull


class HL7_SI(HL7DataType):
    component_map = ['sequence_id']


class HL7_ExtendedCompositeId(HL7DataType):
    """ CX extended composite id with check digit """

    field_map = [
        make_cell_type('id_number', options={"reqired": True}),
        make_cell_type('identifier_check_digit'),
        make_cell_type('check_digit_scheme'),
        make_cell_type('assigning_authority'),
        make_cell_type('identifier_type_code', options={"required": True}),
        make_cell_type('assigning_facility'),
        make_cell_type('effective_date', options={"type": HL7Datetime}),
        make_cell_type('expiration_date', options={"type": HL7Datetime}),
        make_cell_type('assigning_jurisdiction'),
        make_cell_type('assigning_agency_or_department'),
        make_cell_type('security_check'),
        make_cell_type('security_check_scheme')
    ]


class HL7_CodedWithException(HL7DataType):
    """ CWE HL7_CodedWithException """

    field_map = [
        make_cell_type('id'),
        make_cell_type('text'),
        make_cell_type('name_of_coding_system'),
        make_cell_type('alternate_identifier'),
        make_cell_type('alternate_text'),
        make_cell_type('name_of_alternate_coding_system'),
        make_cell_type('coding_system_version_id'),
        make_cell_type('alternate_coding_system_version_id'),
        make_cell_type('original_text')
        # NOTE: standard defines more fields which can be added if needed in
        # the future
    ]


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
        make_cell_type('street_address', options={"type": HL7_StreetAddress}),
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
        make_cell_type('effective_date', options={"type": HL7Datetime}),
        make_cell_type('expiration_date', options={"type": HL7Datetime}),
        make_cell_type('expiration_reason'),
        make_cell_type('bad_address_indicator'),
        make_cell_type('address_usage'),
        make_cell_type('addressee'),
        make_cell_type('comment'),
        make_cell_type('preference_order'),
        make_cell_type('protection_code'),
        make_cell_type('address_identifier')
    ]


class HL7_ProcessingType(HL7DataType):
    """ PT Processing type """
    field_map = [
        make_cell_type('processing_id', options={"required": True}),
        make_cell_type('processing_mode')
    ]


class HL7_VersionIdentifier(HL7DataType):
    """ VID version identifier """

    field_map = [
        make_cell_type('version_id', options={"required": True}),
        make_cell_type('internationalization_code',
                       options={"type": HL7_CodedWithException}),
        make_cell_type('international_version_id',
                       options={"type": HL7_CodedWithException}),

    ]


class HL7_MessageType(HL7DataType):
    """ MSG Message Type """

    field_map = [
        make_cell_type('message_code', options={"required": True}),
        make_cell_type('trigger_event', options={"required": True}),
        make_cell_type('message_structure', options={"required": True})
    ]


class HL7_PersonLocation(HL7DataType):
    """ PL person location """

    field_map = [
        make_cell_type('point_of_care'),
        make_cell_type('room'),
        make_cell_type('bed'),
        make_cell_type('facility'),
        make_cell_type('location_status'),
        make_cell_type('person_location_type'),
        make_cell_type('building'),
        make_cell_type('floor'),
        make_cell_type('location_description'),
        make_cell_type('comprehensive_location_identifier'),
        make_cell_type('assigning_authority_for_location'),
    ]


class HL7_XCN_ExtendedCompositeID(HL7DataType):
    """ XCN extended composite ID number and name for persons """
    field_map = [
        make_cell_type("person_identifier"),
        make_cell_type("family_name"),
        make_cell_type("given_name"),
        make_cell_type("second_name"),
        make_cell_type("suffix"),
        make_cell_type("prefix"),
        make_cell_type("degree"),
        # NOTE: standard defines more fields which can be added if needed in
        # the future
    ]


class HL7_FinancialClass(HL7DataType):
    """ FC financial class """
    field_map = [
        make_cell_type("financial_class_code", options={"type": HL7_CodedWithException}),
        make_cell_type("effective_date", options={"type": HL7Datetime}),
    ]
