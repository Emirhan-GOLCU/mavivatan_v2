// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from zed_msgs:srv/SaveAreaMemory.idl
// generated code does not contain a copyright notice

#ifndef ZED_MSGS__SRV__DETAIL__SAVE_AREA_MEMORY__STRUCT_HPP_
#define ZED_MSGS__SRV__DETAIL__SAVE_AREA_MEMORY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__zed_msgs__srv__SaveAreaMemory_Request __attribute__((deprecated))
#else
# define DEPRECATED__zed_msgs__srv__SaveAreaMemory_Request __declspec(deprecated)
#endif

namespace zed_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SaveAreaMemory_Request_
{
  using Type = SaveAreaMemory_Request_<ContainerAllocator>;

  explicit SaveAreaMemory_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->area_file_path = "";
    }
  }

  explicit SaveAreaMemory_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : area_file_path(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->area_file_path = "";
    }
  }

  // field types and members
  using _area_file_path_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _area_file_path_type area_file_path;

  // setters for named parameter idiom
  Type & set__area_file_path(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->area_file_path = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__zed_msgs__srv__SaveAreaMemory_Request
    std::shared_ptr<zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__zed_msgs__srv__SaveAreaMemory_Request
    std::shared_ptr<zed_msgs::srv::SaveAreaMemory_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SaveAreaMemory_Request_ & other) const
  {
    if (this->area_file_path != other.area_file_path) {
      return false;
    }
    return true;
  }
  bool operator!=(const SaveAreaMemory_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SaveAreaMemory_Request_

// alias to use template instance with default allocator
using SaveAreaMemory_Request =
  zed_msgs::srv::SaveAreaMemory_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace zed_msgs


#ifndef _WIN32
# define DEPRECATED__zed_msgs__srv__SaveAreaMemory_Response __attribute__((deprecated))
#else
# define DEPRECATED__zed_msgs__srv__SaveAreaMemory_Response __declspec(deprecated)
#endif

namespace zed_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SaveAreaMemory_Response_
{
  using Type = SaveAreaMemory_Response_<ContainerAllocator>;

  explicit SaveAreaMemory_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit SaveAreaMemory_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__zed_msgs__srv__SaveAreaMemory_Response
    std::shared_ptr<zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__zed_msgs__srv__SaveAreaMemory_Response
    std::shared_ptr<zed_msgs::srv::SaveAreaMemory_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SaveAreaMemory_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const SaveAreaMemory_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SaveAreaMemory_Response_

// alias to use template instance with default allocator
using SaveAreaMemory_Response =
  zed_msgs::srv::SaveAreaMemory_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace zed_msgs

namespace zed_msgs
{

namespace srv
{

struct SaveAreaMemory
{
  using Request = zed_msgs::srv::SaveAreaMemory_Request;
  using Response = zed_msgs::srv::SaveAreaMemory_Response;
};

}  // namespace srv

}  // namespace zed_msgs

#endif  // ZED_MSGS__SRV__DETAIL__SAVE_AREA_MEMORY__STRUCT_HPP_
