#include "ctc_sai_platform.h"
#include "ctc_board_types.h"

/******************************************************************************
 * e530_24x2c
 ******************************************************************************/

#define E530_24X2C_FIBER_NUM 26
#define E530_24X2C_LED_MAC_NUM 26
#define E530_24X2C_LED_FANOUT_NUM 4


fiber_info_t e530_24x2c_fiber_table[E530_24X2C_FIBER_NUM] =
{
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 0}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp1/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp1/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
      
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 1}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp2/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp2/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 7}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp3/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp3/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 6}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp4/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp4/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 5}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp5/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp5/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 2}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp6/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp6/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 4}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp7/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp7/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 3}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp8/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp8/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 8}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp9/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp9/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 9}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp10/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp10/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 15}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp11/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp11/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 14}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp12/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp12/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 13}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp13/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp13/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 10}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp14/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp14/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 12}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp15/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp15/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 11}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp16/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp16/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },


    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 20}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp17/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp17/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 19}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp18/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp18/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 21}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp19/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp19/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 18}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp20/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp20/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 22}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp21/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp21/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 17}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp22/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp22/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 23}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp23/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp23/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 16}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp24/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp24/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },

    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_QSFP_P,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 24}},
                              .en_mode   = E_FIBER_EN_QSFP,
                              .en        = {.en_qsfp = {0}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp25/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_QSFP_P,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 25}},
                              .en_mode   = E_FIBER_EN_QSFP,
                              .en        = {.en_qsfp = {0}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp26/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
};

macled_info_t e530_24x2c_macled_info;

mac_led_api_para_t e530_24x2c_mac_led_default_entry[E530_24X2C_LED_MAC_NUM + E530_24X2C_LED_FANOUT_NUM] =
{
    /* panel port 49-52 */
    {
      .port_id = 67,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_1_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 66,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_1_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 65,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_1_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 64,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_1_FORCE_OFF,
      .fixed   = 0,
    },
    
    {
      .port_id = 44,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 60,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },

    {
      .port_id = 31,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 30,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 29,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 28,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 27,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 26,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 25,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 24,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },

    {
      .port_id = 15,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 14,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 13,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 12,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 23,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 22,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 21,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 20,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },   

    {
      .port_id = 11,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 10,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 9,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 8,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 3,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 2,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 1,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 0,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
};

led2mac_t e530_24x2c_led2mac[E530_24X2C_LED_MAC_NUM] =
{
    {
      .sysfs = "/sys/class/leds/port1/brightness",
      .para  = {
                 .port_id = 0,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port2/brightness",
      .para  = {
                 .port_id = 1,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port3/brightness",
      .para  = {
                 .port_id = 2,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port4/brightness",
      .para  = {
                 .port_id = 3,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port5/brightness",
      .para  = {
                 .port_id = 8,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port6/brightness",
      .para  = {
                 .port_id = 9,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port7/brightness",
      .para  = {
                 .port_id = 10,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port8/brightness",
      .para  = {
                 .port_id = 11,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port9/brightness",
      .para  = {
                 .port_id = 20,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port10/brightness",
      .para  = {
                 .port_id = 21,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port11/brightness",
      .para  = {
                 .port_id = 22,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port12/brightness",
      .para  = {
                 .port_id = 23,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port13/brightness",
      .para  = {
                 .port_id = 12,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port14/brightness",
      .para  = {
                 .port_id = 13,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port15/brightness",
      .para  = {
                 .port_id = 14,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port16/brightness",
      .para  = {
                 .port_id = 15,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
                 
    {
      .sysfs = "/sys/class/leds/port17/brightness",
      .para  = {
                 .port_id = 24,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port18/brightness",
      .para  = {
                 .port_id = 25,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port19/brightness",
      .para  = {
                 .port_id = 26,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port20/brightness",
      .para  = {
                 .port_id = 27,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port21/brightness",
      .para  = {
                 .port_id = 28,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port22/brightness",
      .para  = {
                 .port_id = 29,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port23/brightness",
      .para  = {
                 .port_id = 30,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port24/brightness",
      .para  = {
                 .port_id = 31,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port25/brightness",
      .para  = {
                 .port_id = 60,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port26/brightness",
      .para  = {
                 .port_id = 44,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
};


int32 ctc_sai_e530_24x2c_create_fiber_handle(glb_card_t *p_glb_card)
{
    int idx = 0;

    p_glb_card->fiber_num = E530_24X2C_FIBER_NUM;
    p_glb_card->fiber_info_table = e530_24x2c_fiber_table;

    for (idx = 0; idx < E530_24X2C_FIBER_NUM; idx++)
    {
        e530_24x2c_fiber_table[idx].fiber_hdl = fiber_create_handle(&(e530_24x2c_fiber_table[idx].fiber_gen));
    }

    return 0;
}

int32 ctc_sai_e530_24x2c_create_macled_handle(glb_card_t *p_glb_card)
{
    p_glb_card->macled_info = &e530_24x2c_macled_info;

    p_glb_card->macled_info->macled_gen.mac_table_id = 0;
    p_glb_card->macled_info->macled_gen.p_mac_led_info = (mac_led_info_t *)mem_malloc(
                                                          MEM_SYSTEM_MODULE, sizeof(mac_led_info_t));
    p_glb_card->macled_info->macled_gen.p_mac_led_info->table_num = 1;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_num = E530_24X2C_LED_MAC_NUM + E530_24X2C_LED_FANOUT_NUM;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->slice0_mac_num = E530_24X2C_LED_MAC_NUM + E530_24X2C_LED_FANOUT_NUM;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->polarity = 1;
    p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_led_api_para = (mac_led_api_para_t **)mem_malloc(
                                                                            MEM_SYSTEM_MODULE,
                                                                            sizeof(mac_led_api_para_t*) *
                                                                            p_glb_card->macled_info->macled_gen.p_mac_led_info->table_num);
    p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_led_api_para[0] = e530_24x2c_mac_led_default_entry;

    
    p_glb_card->macled_info->macled_hdl = macled_create_handle(&(p_glb_card->macled_info->macled_gen));


    if (p_glb_card->macled_info->macled_hdl != NULL)
        p_glb_card->macled_info->macled_hdl->init(p_glb_card->macled_info->macled_hdl);

    p_glb_card->macled_info->led2mac = (led2mac_t *)mem_malloc(MEM_SYSTEM_MODULE, sizeof(led2mac_t) * E530_24X2C_LED_MAC_NUM);
    p_glb_card->macled_info->led2mac_size = E530_24X2C_LED_MAC_NUM;
    sal_memcpy(p_glb_card->macled_info->led2mac, e530_24x2c_led2mac, sizeof(led2mac_t) * E530_24X2C_LED_MAC_NUM);
    
    return 0;
}

void ctc_sai_e530_24x2c_platform_callback(void)
{
    int32 temp = -1000;
    FILE *fp = NULL;

    ctcs_get_chip_sensor(0, CTC_CHIP_SENSOR_TEMP, (uint32 *)&temp);

    if (temp >= -40 && temp <= 125)
    {
        fp = sal_fopen("/sys/class/hwmon/hwmon0/temp1_input", "w");
        if (fp == NULL)
        {
            return;
        }
        fprintf(fp, "%d", temp * 1000);
        sal_fclose(fp);
    }

    return;
}

int32 ctc_sai_e530_24x2c_board_init(glb_card_t *p_glb_card)
{
    int ret = 0;

    ret += ctc_sai_e530_24x2c_create_fiber_handle(p_glb_card);
    ret += ctc_sai_e530_24x2c_create_macled_handle(p_glb_card);
    p_glb_card->platform_callback = ctc_sai_e530_24x2c_platform_callback;

    return ret;
}
