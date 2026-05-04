// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from mavivatan_interfaces:msg/IdaDurum.idl
// generated code does not contain a copyright notice

#ifndef MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "mavivatan_interfaces/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "mavivatan_interfaces/msg/detail/ida_durum__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace mavivatan_interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mavivatan_interfaces
cdr_serialize(
  const mavivatan_interfaces::msg::IdaDurum & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mavivatan_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  mavivatan_interfaces::msg::IdaDurum & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mavivatan_interfaces
get_serialized_size(
  const mavivatan_interfaces::msg::IdaDurum & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mavivatan_interfaces
max_serialized_size_IdaDurum(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace mavivatan_interfaces

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_mavivatan_interfaces
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, mavivatan_interfaces, msg, IdaDurum)();

#ifdef __cplusplus
}
#endif

#endif  // MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
