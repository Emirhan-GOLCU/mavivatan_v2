// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from mavivatan_interfaces:msg/IdaDurum.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "mavivatan_interfaces/msg/detail/ida_durum__struct.h"
#include "mavivatan_interfaces/msg/detail/ida_durum__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool mavivatan_interfaces__msg__ida_durum__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[45];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("mavivatan_interfaces.msg._ida_durum.IdaDurum", full_classname_dest, 44) == 0);
  }
  mavivatan_interfaces__msg__IdaDurum * ros_message = _ros_message;
  {  // hiz
    PyObject * field = PyObject_GetAttrString(_pymsg, "hiz");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->hiz = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // batarya
    PyObject * field = PyObject_GetAttrString(_pymsg, "batarya");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->batarya = PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // mod
    PyObject * field = PyObject_GetAttrString(_pymsg, "mod");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->mod, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * mavivatan_interfaces__msg__ida_durum__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of IdaDurum */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("mavivatan_interfaces.msg._ida_durum");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "IdaDurum");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  mavivatan_interfaces__msg__IdaDurum * ros_message = (mavivatan_interfaces__msg__IdaDurum *)raw_ros_message;
  {  // hiz
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->hiz);
    {
      int rc = PyObject_SetAttrString(_pymessage, "hiz", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // batarya
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->batarya);
    {
      int rc = PyObject_SetAttrString(_pymessage, "batarya", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // mod
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->mod.data,
      strlen(ros_message->mod.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "mod", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
