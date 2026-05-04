// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from mavivatan_interfaces:msg/IdaDurum.idl
// generated code does not contain a copyright notice

#ifndef MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__STRUCT_HPP_
#define MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__mavivatan_interfaces__msg__IdaDurum __attribute__((deprecated))
#else
# define DEPRECATED__mavivatan_interfaces__msg__IdaDurum __declspec(deprecated)
#endif

namespace mavivatan_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct IdaDurum_
{
  using Type = IdaDurum_<ContainerAllocator>;

  explicit IdaDurum_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->hiz = 0.0;
      this->batarya = 0.0;
      this->mod = "";
    }
  }

  explicit IdaDurum_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : mod(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->hiz = 0.0;
      this->batarya = 0.0;
      this->mod = "";
    }
  }

  // field types and members
  using _hiz_type =
    double;
  _hiz_type hiz;
  using _batarya_type =
    double;
  _batarya_type batarya;
  using _mod_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _mod_type mod;

  // setters for named parameter idiom
  Type & set__hiz(
    const double & _arg)
  {
    this->hiz = _arg;
    return *this;
  }
  Type & set__batarya(
    const double & _arg)
  {
    this->batarya = _arg;
    return *this;
  }
  Type & set__mod(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->mod = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator> *;
  using ConstRawPtr =
    const mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__mavivatan_interfaces__msg__IdaDurum
    std::shared_ptr<mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__mavivatan_interfaces__msg__IdaDurum
    std::shared_ptr<mavivatan_interfaces::msg::IdaDurum_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const IdaDurum_ & other) const
  {
    if (this->hiz != other.hiz) {
      return false;
    }
    if (this->batarya != other.batarya) {
      return false;
    }
    if (this->mod != other.mod) {
      return false;
    }
    return true;
  }
  bool operator!=(const IdaDurum_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct IdaDurum_

// alias to use template instance with default allocator
using IdaDurum =
  mavivatan_interfaces::msg::IdaDurum_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace mavivatan_interfaces

#endif  // MAVIVATAN_INTERFACES__MSG__DETAIL__IDA_DURUM__STRUCT_HPP_
