# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: POGOProtos/Enums/PokemonClass.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='POGOProtos/Enums/PokemonClass.proto',
  package='POGOProtos.Enums',
  syntax='proto3',
  serialized_pb=_b('\n#POGOProtos/Enums/PokemonClass.proto\x12\x10POGOProtos.Enums*5\n\x0cPokemonClass\x12\n\n\x06NORMAL\x10\x00\x12\r\n\tLEGENDARY\x10\x01\x12\n\n\x06MYTHIC\x10\x02\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

_POKEMONCLASS = _descriptor.EnumDescriptor(
  name='PokemonClass',
  full_name='POGOProtos.Enums.PokemonClass',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='NORMAL', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LEGENDARY', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MYTHIC', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=57,
  serialized_end=110,
)
_sym_db.RegisterEnumDescriptor(_POKEMONCLASS)

PokemonClass = enum_type_wrapper.EnumTypeWrapper(_POKEMONCLASS)
NORMAL = 0
LEGENDARY = 1
MYTHIC = 2


DESCRIPTOR.enum_types_by_name['PokemonClass'] = _POKEMONCLASS


# @@protoc_insertion_point(module_scope)
