# hl7parser - Parse HL7-Messages in Python

[![Build Status](https://travis-ci.org/mps-gmbh/hl7-parser.svg?branch=master)](https://travis-ci.org/mps-gmbh/hl7-parser)

`hl7-parser` is a parser for HL7 ([Health Level 7](https://en.wikipedia.org/wiki/Health_Level_7)) messages. It also has limited support for constructing messages.

To see what's new in each version, please refer to the `CHANGELOG.md` file in the repository.

## Installation

`hl7parser` is available through PyPi and can be installed using pip: `pip install hl7-parser`

It supports Python 2.7 and Python >=3.5 (as of version 0.7).

## Usage

#### Parsing Messages

```python
# This is an example message taken from the HL7 Wikipedia article
>>> message_text = """
... MSH|^~\&|MegaReg|XYZHospC|SuperOE|XYZImgCtr|20060529090131-0500||ADT^A01^ADT_A01|01052901|P|2.5
... EVN||200605290901||||200605290900
... PID|||56782445^^^UAReg^PI||KLEINSAMPLE^BARRY^Q^JR||19620910|M||2028-9^^HL70005^RA99113^^XYZ|260 GOODWIN CREST DRIVE^^BIRMINGHAM^AL^35209^^M~NICKELL’S PICKLES^10000 W 100TH AVE^BIRMINGHAM^AL^35200^^O|||||||0105I30001^^^99DEF^AN
... PV1||I|W^389^1^UABH^^^^3||||12345^MORGAN^REX^J^^^MD^0010^UAMC^L||67890^GRAINGER^LUCY^X^^^MD^0010^UAMC^L|MED|||||A0||13579^POTTER^SHERMAN^T^^^MD^0010^UAMC^L|||||||||||||||||||||||||||200605290900
... OBX|1|NM|^Body Height||1.80|m^Meter^ISO+|||||F
... OBX|2|NM|^Body Weight||79|kg^Kilogram^ISO+|||||F
... AL1|1||^ASPIRIN
... DG1|1||786.50^CHEST PAIN, UNSPECIFIED^I9|||A
... """.strip()

>>> from hl7parser.hl7 import HL7Message
>>> msg = HL7Message(message_text)
# access segments and their fields by name
>>> msg.evn.recorded_datetime.isoformat()
'2006-05-29T09:01:00'
# .. or index (
>>> msg.evn[1].isoformat()
'2006-05-29T09:01:00'

# repeating fields
>>> str(msg.pid.patient_name[0])
'KLEINSAMPLE^BARRY^Q^JR'
# subfields
>>> str(msg.pid.patient_name[0][1])
'BARRY'
```

Some common segments are pre-defined and `hl7parser` will validate input on the fields:

* MSH - Message Header
* MSA - Message Acknowledgement
* EVN - Event Type
* PID - Patient Identification
* PV1 - Patient Visit
* and others

Segments which are not defined, will still work, but will lack input validation and you won't be able to access fields by name.

If you need support for other segments, file an issue or send a pull request.
