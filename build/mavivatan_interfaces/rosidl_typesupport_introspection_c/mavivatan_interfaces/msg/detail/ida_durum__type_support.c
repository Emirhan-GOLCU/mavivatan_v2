// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from mavivatan_interfaces:msg/IdaDurum.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "mavivatan_interfaces/msg/detail/ida_durum__rosidl_typesupport_introspection_c.h"
#include "mavivatan_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "mavivatan_interfaces/msg/detail/ida_durum__functions.h"
#include "mavivatan_interfaces/msg/detail/ida_durum__struct.h"


// Include directives for member types
// Member `mod`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  mavivatan_interfaces__msg__IdaDurum__init(message_memory);
}

void mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_fini_function(void * message_memory)
{
  mavivatan_interfaces__msg__IdaDurum__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_message_member_array[3] = {
  {
    "hiz",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mavivatan_interfaces__msg__IdaDurum, hiz),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "batarya",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mavivatan_interfaces__msg__IdaDurum, batarya),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "mod",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(mavivatan_interfaces__msg__IdaDurum, mod),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_message_members = {
  "mavivatan_interfaces__msg",  // message namespace
  "IdaDurum",  // message name
  3,  // number of fields
  sizeof(mavivatan_interfaces__msg__IdaDurum),
  mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_message_member_array,  // message members
  mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_init_function,  // function to initialize message memory (memory has to be allocated)
  mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_message_type_support_handle = {
  0,
  &mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_mavivatan_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, mavivatan_interfaces, msg, IdaDurum)() {
  if (!mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_message_type_support_handle.typesupport_identifier) {
    mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &mavivatan_interfaces__msg__IdaDurum__rosidl_typesupport_introspection_c__IdaDurum_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
