// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from zed_msgs:srv/SaveAreaMemory.idl
// generated code does not contain a copyright notice

#ifndef ZED_MSGS__SRV__DETAIL__SAVE_AREA_MEMORY__STRUCT_H_
#define ZED_MSGS__SRV__DETAIL__SAVE_AREA_MEMORY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'area_file_path'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SaveAreaMemory in the package zed_msgs.
typedef struct zed_msgs__srv__SaveAreaMemory_Request
{
  /// Path of an area localization file that describes the surroundings. Use ".area" extension.
  rosidl_runtime_c__String area_file_path;
} zed_msgs__srv__SaveAreaMemory_Request;

// Struct for a sequence of zed_msgs__srv__SaveAreaMemory_Request.
typedef struct zed_msgs__srv__SaveAreaMemory_Request__Sequence
{
  zed_msgs__srv__SaveAreaMemory_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} zed_msgs__srv__SaveAreaMemory_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SaveAreaMemory in the package zed_msgs.
typedef struct zed_msgs__srv__SaveAreaMemory_Response
{
  /// indicate successful run of service
  bool success;
  /// informational, e.g. for error messages
  rosidl_runtime_c__String message;
} zed_msgs__srv__SaveAreaMemory_Response;

// Struct for a sequence of zed_msgs__srv__SaveAreaMemory_Response.
typedef struct zed_msgs__srv__SaveAreaMemory_Response__Sequence
{
  zed_msgs__srv__SaveAreaMemory_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} zed_msgs__srv__SaveAreaMemory_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ZED_MSGS__SRV__DETAIL__SAVE_AREA_MEMORY__STRUCT_H_
