# coding: utf-8 
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: base/v1/base.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='base/v1/base.proto',
  package='didi.cloud.base.v1',
  syntax='proto3',
  serialized_options=_b('\n\023com.didiyun.base.v1B\004BaseP\001Z.github.com/didiyun/didiyun-go-sdk/base/v1;base\370\001\001\252\002\022Didi.Cloud.Base.V1\312\002\022Didi\\Cloud\\Base\\V1'),
  serialized_pb=_b('\n\x12\x62\x61se/v1/base.proto\x12\x12\x64idi.cloud.base.v1\"9\n\x05\x45rror\x12\r\n\x05\x65rrno\x18\x01 \x01(\x05\x12\x0e\n\x06\x65rrmsg\x18\x02 \x01(\t\x12\x11\n\trequestId\x18\x03 \x01(\t\"*\n\x06Header\x12\x10\n\x08regionId\x18\x01 \x01(\t\x12\x0e\n\x06zoneId\x18\x02 \x01(\t\"\x7f\n\x07JobInfo\x12\x0f\n\x07jobUuid\x18\x01 \x01(\t\x12\x14\n\x0cresourceUuid\x18\x02 \x01(\t\x12\x10\n\x08progress\x18\x03 \x01(\x01\x12\x0c\n\x04type\x18\x04 \x01(\t\x12\x0c\n\x04\x64one\x18\x05 \x01(\x08\x12\x0f\n\x07success\x18\x06 \x01(\x08\x12\x0e\n\x06result\x18\x07 \x01(\t\"8\n\nRegionInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08\x61reaName\x18\x03 \x01(\t\"$\n\x08ZoneInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\"k\n\x11RegionAndZoneInfo\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08\x61reaName\x18\x03 \x01(\t\x12*\n\x04zone\x18\x05 \x01(\x0b\x32\x1c.didi.cloud.base.v1.ZoneInfoBz\n\x13\x63om.didiyun.base.v1B\x04\x42\x61seP\x01Z.github.com/didiyun/didiyun-go-sdk/base/v1;base\xf8\x01\x01\xaa\x02\x12\x44idi.Cloud.Base.V1\xca\x02\x12\x44idi\\Cloud\\Base\\V1b\x06proto3')
)




_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='didi.cloud.base.v1.Error',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='errno', full_name='didi.cloud.base.v1.Error.errno', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='errmsg', full_name='didi.cloud.base.v1.Error.errmsg', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='requestId', full_name='didi.cloud.base.v1.Error.requestId', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=42,
  serialized_end=99,
)


_HEADER = _descriptor.Descriptor(
  name='Header',
  full_name='didi.cloud.base.v1.Header',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='regionId', full_name='didi.cloud.base.v1.Header.regionId', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zoneId', full_name='didi.cloud.base.v1.Header.zoneId', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=101,
  serialized_end=143,
)


_JOBINFO = _descriptor.Descriptor(
  name='JobInfo',
  full_name='didi.cloud.base.v1.JobInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='jobUuid', full_name='didi.cloud.base.v1.JobInfo.jobUuid', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='resourceUuid', full_name='didi.cloud.base.v1.JobInfo.resourceUuid', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='progress', full_name='didi.cloud.base.v1.JobInfo.progress', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='didi.cloud.base.v1.JobInfo.type', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='done', full_name='didi.cloud.base.v1.JobInfo.done', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='success', full_name='didi.cloud.base.v1.JobInfo.success', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result', full_name='didi.cloud.base.v1.JobInfo.result', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=145,
  serialized_end=272,
)


_REGIONINFO = _descriptor.Descriptor(
  name='RegionInfo',
  full_name='didi.cloud.base.v1.RegionInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='didi.cloud.base.v1.RegionInfo.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='didi.cloud.base.v1.RegionInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='areaName', full_name='didi.cloud.base.v1.RegionInfo.areaName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=274,
  serialized_end=330,
)


_ZONEINFO = _descriptor.Descriptor(
  name='ZoneInfo',
  full_name='didi.cloud.base.v1.ZoneInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='didi.cloud.base.v1.ZoneInfo.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='didi.cloud.base.v1.ZoneInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=332,
  serialized_end=368,
)


_REGIONANDZONEINFO = _descriptor.Descriptor(
  name='RegionAndZoneInfo',
  full_name='didi.cloud.base.v1.RegionAndZoneInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='didi.cloud.base.v1.RegionAndZoneInfo.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='didi.cloud.base.v1.RegionAndZoneInfo.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='areaName', full_name='didi.cloud.base.v1.RegionAndZoneInfo.areaName', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zone', full_name='didi.cloud.base.v1.RegionAndZoneInfo.zone', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=370,
  serialized_end=477,
)

_REGIONANDZONEINFO.fields_by_name['zone'].message_type = _ZONEINFO
DESCRIPTOR.message_types_by_name['Error'] = _ERROR
DESCRIPTOR.message_types_by_name['Header'] = _HEADER
DESCRIPTOR.message_types_by_name['JobInfo'] = _JOBINFO
DESCRIPTOR.message_types_by_name['RegionInfo'] = _REGIONINFO
DESCRIPTOR.message_types_by_name['ZoneInfo'] = _ZONEINFO
DESCRIPTOR.message_types_by_name['RegionAndZoneInfo'] = _REGIONANDZONEINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), dict(
  DESCRIPTOR = _ERROR,
  __module__ = 'base.v1.base_pb2'
  # @@protoc_insertion_point(class_scope:didi.cloud.base.v1.Error)
  ))
_sym_db.RegisterMessage(Error)

Header = _reflection.GeneratedProtocolMessageType('Header', (_message.Message,), dict(
  DESCRIPTOR = _HEADER,
  __module__ = 'base.v1.base_pb2'
  # @@protoc_insertion_point(class_scope:didi.cloud.base.v1.Header)
  ))
_sym_db.RegisterMessage(Header)

JobInfo = _reflection.GeneratedProtocolMessageType('JobInfo', (_message.Message,), dict(
  DESCRIPTOR = _JOBINFO,
  __module__ = 'base.v1.base_pb2'
  # @@protoc_insertion_point(class_scope:didi.cloud.base.v1.JobInfo)
  ))
_sym_db.RegisterMessage(JobInfo)

RegionInfo = _reflection.GeneratedProtocolMessageType('RegionInfo', (_message.Message,), dict(
  DESCRIPTOR = _REGIONINFO,
  __module__ = 'base.v1.base_pb2'
  # @@protoc_insertion_point(class_scope:didi.cloud.base.v1.RegionInfo)
  ))
_sym_db.RegisterMessage(RegionInfo)

ZoneInfo = _reflection.GeneratedProtocolMessageType('ZoneInfo', (_message.Message,), dict(
  DESCRIPTOR = _ZONEINFO,
  __module__ = 'base.v1.base_pb2'
  # @@protoc_insertion_point(class_scope:didi.cloud.base.v1.ZoneInfo)
  ))
_sym_db.RegisterMessage(ZoneInfo)

RegionAndZoneInfo = _reflection.GeneratedProtocolMessageType('RegionAndZoneInfo', (_message.Message,), dict(
  DESCRIPTOR = _REGIONANDZONEINFO,
  __module__ = 'base.v1.base_pb2'
  # @@protoc_insertion_point(class_scope:didi.cloud.base.v1.RegionAndZoneInfo)
  ))
_sym_db.RegisterMessage(RegionAndZoneInfo)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
