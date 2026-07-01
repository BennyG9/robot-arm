// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from arm_interfaces:srv/Calibrate.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACES__SRV__DETAIL__CALIBRATE__TRAITS_HPP_
#define ARM_INTERFACES__SRV__DETAIL__CALIBRATE__TRAITS_HPP_

#include "arm_interfaces/srv/detail/calibrate__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_interfaces::srv::Calibrate_Request>()
{
  return "arm_interfaces::srv::Calibrate_Request";
}

template<>
inline const char * name<arm_interfaces::srv::Calibrate_Request>()
{
  return "arm_interfaces/srv/Calibrate_Request";
}

template<>
struct has_fixed_size<arm_interfaces::srv::Calibrate_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<arm_interfaces::srv::Calibrate_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<arm_interfaces::srv::Calibrate_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_interfaces::srv::Calibrate_Response>()
{
  return "arm_interfaces::srv::Calibrate_Response";
}

template<>
inline const char * name<arm_interfaces::srv::Calibrate_Response>()
{
  return "arm_interfaces/srv/Calibrate_Response";
}

template<>
struct has_fixed_size<arm_interfaces::srv::Calibrate_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<arm_interfaces::srv::Calibrate_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<arm_interfaces::srv::Calibrate_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<arm_interfaces::srv::Calibrate>()
{
  return "arm_interfaces::srv::Calibrate";
}

template<>
inline const char * name<arm_interfaces::srv::Calibrate>()
{
  return "arm_interfaces/srv/Calibrate";
}

template<>
struct has_fixed_size<arm_interfaces::srv::Calibrate>
  : std::integral_constant<
    bool,
    has_fixed_size<arm_interfaces::srv::Calibrate_Request>::value &&
    has_fixed_size<arm_interfaces::srv::Calibrate_Response>::value
  >
{
};

template<>
struct has_bounded_size<arm_interfaces::srv::Calibrate>
  : std::integral_constant<
    bool,
    has_bounded_size<arm_interfaces::srv::Calibrate_Request>::value &&
    has_bounded_size<arm_interfaces::srv::Calibrate_Response>::value
  >
{
};

template<>
struct is_service<arm_interfaces::srv::Calibrate>
  : std::true_type
{
};

template<>
struct is_service_request<arm_interfaces::srv::Calibrate_Request>
  : std::true_type
{
};

template<>
struct is_service_response<arm_interfaces::srv::Calibrate_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // ARM_INTERFACES__SRV__DETAIL__CALIBRATE__TRAITS_HPP_
