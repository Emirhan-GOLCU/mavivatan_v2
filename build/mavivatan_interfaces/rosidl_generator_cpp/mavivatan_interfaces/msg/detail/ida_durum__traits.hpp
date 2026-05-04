// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from mavivatan_interfaces:msg/IdaDurum.idl
// generated code does not contain a copyright notice

#ifndef MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__TRAITS_HPP_
#define MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "mavivatan_interfaces/msg/detail/ida_durum__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace mavivatan_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const IdaDurum & msg,
  std::ostream & out)
{
  out << "{";
  // member: hiz
  {
    out << "hiz: ";
    rosidl_generator_traits::value_to_yaml(msg.hiz, out);
    out << ", ";
  }

  // member: batarya
  {
    out << "batarya: ";
    rosidl_generator_traits::value_to_yaml(msg.batarya, out);
    out << ", ";
  }

  // member: mod
  {
    out << "mod: ";
    rosidl_generator_traits::value_to_yaml(msg.mod, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const IdaDurum & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: hiz
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "hiz: ";
    rosidl_generator_traits::value_to_yaml(msg.hiz, out);
    out << "\n";
  }

  // member: batarya
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "batarya: ";
    rosidl_generator_traits::value_to_yaml(msg.batarya, out);
    out << "\n";
  }

  // member: mod
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "mod: ";
    rosidl_generator_traits::value_to_yaml(msg.mod, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const IdaDurum & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace mavivatan_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use mavivatan_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const mavivatan_interfaces::msg::IdaDurum & msg,
  std::ostream & out, size_t indentation = 0)
{
  mavivatan_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use mavivatan_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const mavivatan_interfaces::msg::IdaDurum & msg)
{
  return mavivatan_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<mavivatan_interfaces::msg::IdaDurum>()
{
  return "mavivatan_interfaces::msg::IdaDurum";
}

template<>
inline const char * name<mavivatan_interfaces::msg::IdaDurum>()
{
  return "mavivatan_interfaces/msg/IdaDurum";
}

template<>
struct has_fixed_size<mavivatan_interfaces::msg::IdaDurum>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<mavivatan_interfaces::msg::IdaDurum>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<mavivatan_interfaces::msg::IdaDurum>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__TRAITS_HPP_
