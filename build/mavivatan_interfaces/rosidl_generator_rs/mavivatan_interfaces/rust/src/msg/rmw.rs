#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "mavivatan_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__mavivatan_interfaces__msg__IdaDurum() -> *const std::ffi::c_void;
}

#[link(name = "mavivatan_interfaces__rosidl_generator_c")]
extern "C" {
    fn mavivatan_interfaces__msg__IdaDurum__init(msg: *mut IdaDurum) -> bool;
    fn mavivatan_interfaces__msg__IdaDurum__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<IdaDurum>, size: usize) -> bool;
    fn mavivatan_interfaces__msg__IdaDurum__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<IdaDurum>);
    fn mavivatan_interfaces__msg__IdaDurum__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<IdaDurum>, out_seq: *mut rosidl_runtime_rs::Sequence<IdaDurum>) -> bool;
}

// Corresponds to mavivatan_interfaces__msg__IdaDurum
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct IdaDurum {

    // This member is not documented.
    #[allow(missing_docs)]
    pub hiz: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub batarya: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub mod_: rosidl_runtime_rs::String,

}



impl Default for IdaDurum {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !mavivatan_interfaces__msg__IdaDurum__init(&mut msg as *mut _) {
        panic!("Call to mavivatan_interfaces__msg__IdaDurum__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for IdaDurum {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mavivatan_interfaces__msg__IdaDurum__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mavivatan_interfaces__msg__IdaDurum__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { mavivatan_interfaces__msg__IdaDurum__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for IdaDurum {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for IdaDurum where Self: Sized {
  const TYPE_NAME: &'static str = "mavivatan_interfaces/msg/IdaDurum";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__mavivatan_interfaces__msg__IdaDurum() }
  }
}


