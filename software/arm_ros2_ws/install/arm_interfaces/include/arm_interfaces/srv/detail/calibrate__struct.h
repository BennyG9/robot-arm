// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from arm_interfaces:srv/Calibrate.idl
// generated code does not contain a copyright notice

#ifndef ARM_INTERFACES__SRV__DETAIL__CALIBRATE__STRUCT_H_
#define ARM_INTERFACES__SRV__DETAIL__CALIBRATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in srv/Calibrate in the package arm_interfaces.
typedef struct arm_interfaces__srv__Calibrate_Request
{
  uint8_t structure_needs_at_least_one_member;
} arm_interfaces__srv__Calibrate_Request;

// Struct for a sequence of arm_interfaces__srv__Calibrate_Request.
typedef struct arm_interfaces__srv__Calibrate_Request__Sequence
{
  arm_interfaces__srv__Calibrate_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_interfaces__srv__Calibrate_Request__Sequence;


// Constants defined in the message

// Struct defined in srv/Calibrate in the package arm_interfaces.
typedef struct arm_interfaces__srv__Calibrate_Response
{
  bool success;
} arm_interfaces__srv__Calibrate_Response;

// Struct for a sequence of arm_interfaces__srv__Calibrate_Response.
typedef struct arm_interfaces__srv__Calibrate_Response__Sequence
{
  arm_interfaces__srv__Calibrate_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} arm_interfaces__srv__Calibrate_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARM_INTERFACES__SRV__DETAIL__CALIBRATE__STRUCT_H_
