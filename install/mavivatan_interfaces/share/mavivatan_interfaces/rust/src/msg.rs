#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to mavivatan_interfaces__msg__IdaDurum

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    pub mod_: std::string::String,

}



impl Default for IdaDurum {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::IdaDurum::default())
  }
}

impl rosidl_runtime_rs::Message for IdaDurum {
  type RmwMsg = super::msg::rmw::IdaDurum;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        hiz: msg.hiz,
        batarya: msg.batarya,
        mod_: msg.mod_.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      hiz: msg.hiz,
      batarya: msg.batarya,
        mod_: msg.mod_.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      hiz: msg.hiz,
      batarya: msg.batarya,
      mod_: msg.mod_.to_string(),
    }
  }
}


