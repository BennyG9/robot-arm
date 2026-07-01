// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from arm_interfaces:srv/Home.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACES__SRV__DETAIL__HOME__BUILDER_HPP_
#define ARM_INTERFACES__SRV__DETAIL__HOME__BUILDER_HPP_

#include "arm_interfaces/srv/detail/home__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace arm_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interfaces::srv::Home_Request>()
{
  return ::arm_interfaces::srv::Home_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace arm_interfaces


namespace arm_interfaces
{

namespace srv
{

namespace builder
{

class Init_Home_Response_success
{
public:
  Init_Home_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::arm_interfaces::srv::Home_Response success(::arm_interfaces::srv::Home_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::arm_interfaces::srv::Home_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::arm_interfaces::srv::Home_Response>()
{
  return arm_interfaces::srv::builder::Init_Home_Response_success();
}

}  // namespace arm_interfaces

#endif  // ARM_INTERFACES__SRV__DETAIL__HOME__BUILDER_HPP_
