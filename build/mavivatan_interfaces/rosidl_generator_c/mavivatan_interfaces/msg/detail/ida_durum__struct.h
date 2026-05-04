// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from mavivatan_interfaces:msg/IdaDurum.idl
// generated code does not contain a copyright notice

#ifndef MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__STRUCT_H_
#define MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'mod'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/IdaDurum in the package mavivatan_interfaces.
typedef struct mavivatan_interfaces__msg__IdaDurum
{
  double hiz;
  double batarya;
  rosidl_runtime_c__String mod;
} mavivatan_interfaces__msg__IdaDurum;

// Struct for a sequence of mavivatan_interfaces__msg__IdaDurum.
typedef struct mavivatan_interfaces__msg__IdaDurum__Sequence
{
  mavivatan_interfaces__msg__IdaDurum * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} mavivatan_interfaces__msg__IdaDurum__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__STRUCT_H_
