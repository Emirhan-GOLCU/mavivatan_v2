// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from mavivatan_interfaces:msg/IdaDurum.idl
// generated code does not contain a copyright notice

#ifndef MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__BUILDER_HPP_
#define MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "mavivatan_interfaces/msg/detail/ida_durum__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace mavivatan_interfaces
{

namespace msg
{

namespace builder
{

class Init_IdaDurum_mod
{
public:
  explicit Init_IdaDurum_mod(::mavivatan_interfaces::msg::IdaDurum & msg)
  : msg_(msg)
  {}
  ::mavivatan_interfaces::msg::IdaDurum mod(::mavivatan_interfaces::msg::IdaDurum::_mod_type arg)
  {
    msg_.mod = std::move(arg);
    return std::move(msg_);
  }

private:
  ::mavivatan_interfaces::msg::IdaDurum msg_;
};

class Init_IdaDurum_batarya
{
public:
  explicit Init_IdaDurum_batarya(::mavivatan_interfaces::msg::IdaDurum & msg)
  : msg_(msg)
  {}
  Init_IdaDurum_mod batarya(::mavivatan_interfaces::msg::IdaDurum::_batarya_type arg)
  {
    msg_.batarya = std::move(arg);
    return Init_IdaDurum_mod(msg_);
  }

private:
  ::mavivatan_interfaces::msg::IdaDurum msg_;
};

class Init_IdaDurum_hiz
{
public:
  Init_IdaDurum_hiz()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_IdaDurum_batarya hiz(::mavivatan_interfaces::msg::IdaDurum::_hiz_type arg)
  {
    msg_.hiz = std::move(arg);
    return Init_IdaDurum_batarya(msg_);
  }

private:
  ::mavivatan_interfaces::msg::IdaDurum msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::mavivatan_interfaces::msg::IdaDurum>()
{
  return mavivatan_interfaces::msg::builder::Init_IdaDurum_hiz();
}

}  // namespace mavivatan_interfaces

#endif  // MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__BUILDER_HPP_
