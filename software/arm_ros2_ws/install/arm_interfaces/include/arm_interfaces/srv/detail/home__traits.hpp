// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from arm_interfaces:srv/Home.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACES__SRV__DETAIL__HOME__TRAITS_HPP_
#define ARM_INTERFACES__SRV__DETAIL__HOME__TRAITS_HPP_

#include "arm_interfaces/srv/detail/home__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_interfaces::srv::Home_Request>()
{
  return "arm_interfaces::srv::Home_Request";
}

template<>
inline const char * name<arm_interfaces::srv::Home_Request>()
{
  return "arm_interfaces/srv/Home_Request";
}

template<>
struct has_fixed_size<arm_interfaces::srv::Home_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<arm_interfaces::srv::Home_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<arm_interfaces::srv::Home_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_interfaces::srv::Home_Response>()
{
  return "arm_interfaces::srv::Home_Response";
}

template<>
inline const char * name<arm_interfaces::srv::Home_Response>()
{
  return "arm_interfaces/srv/Home_Response";
}

template<>
struct has_fixed_size<arm_interfaces::srv::Home_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<arm_interfaces::srv::Home_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<arm_interfaces::srv::Home_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_interfaces::srv::Home>()
{
  return "arm_interfaces::srv::Home";
}

template<>
inline const char * name<arm_interfaces::srv::Home>()
{
  return "arm_interfaces/srv/Home";
}

template<>
struct has_fixed_size<arm_interfaces::srv::Home>
  : std::integral_constant<
    bool,
    has_fixed_size<arm_interfaces::srv::Home_Request>::value &&
    has_fixed_size<arm_interfaces::srv::Home_Response>::value
  >
{
};

template<>
struct has_bounded_size<arm_interfaces::srv::Home>
  : std::integral_constant<
    bool,
    has_bounded_size<arm_interfaces::srv::Home_Request>::value &&
    has_bounded_size<arm_interfaces::srv::Home_Response>::value
  >
{
};

template<>
struct is_service<arm_interfaces::srv::Home>
  : std::true_type
{
};

template<>
struct is_service_request<arm_interfaces::srv::Home_Request>
  : std::true_type
{
};

template<>
struct is_service_response<arm_interfaces::srv::Home_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ARM_INTERFACES__SRV__DETAIL__HOME__TRAITS_HPP_
