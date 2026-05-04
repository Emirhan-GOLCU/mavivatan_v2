// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from mavivatan_interfaces:msg/IdaDurum.idl
// generated code does not contain a copyright notice
#include "mavivatan_interfaces/msg/detail/ida_durum__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `mod`
#include "rosidl_runtime_c/string_functions.h"

bool
mavivatan_interfaces__msg__IdaDurum__init(mavivatan_interfaces__msg__IdaDurum * msg)
{
  if (!msg) {
    return false;
  }
  // hiz
  // batarya
  // mod
  if (!rosidl_runtime_c__String__init(&msg->mod)) {
    mavivatan_interfaces__msg__IdaDurum__fini(msg);
    return false;
  }
  return true;
}

void
mavivatan_interfaces__msg__IdaDurum__fini(mavivatan_interfaces__msg__IdaDurum * msg)
{
  if (!msg) {
    return;
  }
  // hiz
  // batarya
  // mod
  rosidl_runtime_c__String__fini(&msg->mod);
}

bool
mavivatan_interfaces__msg__IdaDurum__are_equal(const mavivatan_interfaces__msg__IdaDurum * lhs, const mavivatan_interfaces__msg__IdaDurum * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // hiz
  if (lhs->hiz != rhs->hiz) {
    return false;
  }
  // batarya
  if (lhs->batarya != rhs->batarya) {
    return false;
  }
  // mod
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->mod), &(rhs->mod)))
  {
    return false;
  }
  return true;
}

bool
mavivatan_interfaces__msg__IdaDurum__copy(
  const mavivatan_interfaces__msg__IdaDurum * input,
  mavivatan_interfaces__msg__IdaDurum * output)
{
  if (!input || !output) {
    return false;
  }
  // hiz
  output->hiz = input->hiz;
  // batarya
  output->batarya = input->batarya;
  // mod
  if (!rosidl_runtime_c__String__copy(
      &(input->mod), &(output->mod)))
  {
    return false;
  }
  return true;
}

mavivatan_interfaces__msg__IdaDurum *
mavivatan_interfaces__msg__IdaDurum__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mavivatan_interfaces__msg__IdaDurum * msg = (mavivatan_interfaces__msg__IdaDurum *)allocator.allocate(sizeof(mavivatan_interfaces__msg__IdaDurum), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(mavivatan_interfaces__msg__IdaDurum));
  bool success = mavivatan_interfaces__msg__IdaDurum__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
mavivatan_interfaces__msg__IdaDurum__destroy(mavivatan_interfaces__msg__IdaDurum * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    mavivatan_interfaces__msg__IdaDurum__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
mavivatan_interfaces__msg__IdaDurum__Sequence__init(mavivatan_interfaces__msg__IdaDurum__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mavivatan_interfaces__msg__IdaDurum * data = NULL;

  if (size) {
    data = (mavivatan_interfaces__msg__IdaDurum *)allocator.zero_allocate(size, sizeof(mavivatan_interfaces__msg__IdaDurum), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = mavivatan_interfaces__msg__IdaDurum__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        mavivatan_interfaces__msg__IdaDurum__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
mavivatan_interfaces__msg__IdaDurum__Sequence__fini(mavivatan_interfaces__msg__IdaDurum__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      mavivatan_interfaces__msg__IdaDurum__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

mavivatan_interfaces__msg__IdaDurum__Sequence *
mavivatan_interfaces__msg__IdaDurum__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  mavivatan_interfaces__msg__IdaDurum__Sequence * array = (mavivatan_interfaces__msg__IdaDurum__Sequence *)allocator.allocate(sizeof(mavivatan_interfaces__msg__IdaDurum__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = mavivatan_interfaces__msg__IdaDurum__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
mavivatan_interfaces__msg__IdaDurum__Sequence__destroy(mavivatan_interfaces__msg__IdaDurum__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    mavivatan_interfaces__msg__IdaDurum__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
mavivatan_interfaces__msg__IdaDurum__Sequence__are_equal(const mavivatan_interfaces__msg__IdaDurum__Sequence * lhs, const mavivatan_interfaces__msg__IdaDurum__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!mavivatan_interfaces__msg__IdaDurum__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
mavivatan_interfaces__msg__IdaDurum__Sequence__copy(
  const mavivatan_interfaces__msg__IdaDurum__Sequence * input,
  mavivatan_interfaces__msg__IdaDurum__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(mavivatan_interfaces__msg__IdaDurum);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    mavivatan_interfaces__msg__IdaDurum * data =
      (mavivatan_interfaces__msg__IdaDurum *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!mavivatan_interfaces__msg__IdaDurum__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          mavivatan_interfaces__msg__IdaDurum__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!mavivatan_interfaces__msg__IdaDurum__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
