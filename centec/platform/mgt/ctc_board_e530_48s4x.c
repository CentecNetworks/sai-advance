#include "ctc_sai_platform.h"
#include "ctc_board_types.h"
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdio.h>

/******************************************************************************
 * e530_48s4x
 ******************************************************************************/

#define E530_48S4X_FIBER_NUM 52

#define E530_48S4X_LED_MAC_NUM 20
#define E530_48S4X_V2_LED_MAC_NUM 52

fiber_info_t e530_48s4x_fiber_table[E530_48S4X_FIBER_NUM] =
{
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 0, 3}},
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
                              .cs        = {.asic = {0, 0, 2}},
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
                              .cs        = {.asic = {0, 0, 1}},
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
                              .cs        = {.asic = {0, 0, 0}},
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
                              .cs        = {.asic = {0, 0, 4}},
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
                              .cs        = {.asic = {0, 0, 5}},
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
                              .cs        = {.asic = {0, 0, 6}},
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
                              .cs        = {.asic = {0, 0, 7}},
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
                              .cs        = {.asic = {0, 0, 15}},
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
                              .cs        = {.asic = {0, 0, 14}},
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
                              .cs        = {.asic = {0, 0, 13}},
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
                              .cs        = {.asic = {0, 0, 12}},
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
                              .cs        = {.asic = {0, 0, 8}},
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
                              .cs        = {.asic = {0, 0, 9}},
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
                              .cs        = {.asic = {0, 0, 10}},
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
                              .cs        = {.asic = {0, 0, 23}},
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
                              .cs        = {.asic = {0, 0, 22}},
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
                              .cs        = {.asic = {0, 0, 20}},
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
                              .cs        = {.asic = {0, 0, 16}},
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
                              .cs        = {.asic = {0, 0, 18}},
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
                              .cs        = {.asic = {0, 0, 19}},
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
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 2}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp25/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp25/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 3}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp26/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp26/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 7}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp27/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp27/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 6}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp28/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp28/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 5}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp29/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp29/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 4}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp30/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp30/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 0}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp31/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp31/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 1}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp32/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp32/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 8}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp33/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp33/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 9}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp34/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp34/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 10}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp35/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp35/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 11}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp36/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp36/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 12}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp37/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp37/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 13}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp38/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp38/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 14}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp39/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp39/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 15}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp40/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp40/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 16}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp41/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp41/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 17}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp42/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp42/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 18}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp43/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp43/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 19}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp44/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp44/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 20}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp45/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp45/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 21}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp46/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp46/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 22}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp47/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp47/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 23}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp48/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp48/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 24}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp49/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp49/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 25}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp50/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp50/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 26}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp51/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp51/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
    {
      .fiber_gen          = {
                              .fiber_flg = E_FIBER_SFP,
                              .mode      = E_FIBER_ASIC_ASIC,
                              .cs        = {.asic = {0, 1, 27}},
                              .en_mode   = E_FIBER_EN_SYSFS,
                              .en        = {.en_sysfs = {"/sys/class/sfp/sfp52/sfp_enable"}},
                            },
      .sysfs_path         = "/sys/class/sfp/sfp52/",
      .fiber_hdl          = NULL,
      .present            = FIBER_ABSENT,
      .sync_fiber_present = 1,
    },
};

macled_info_t e530_48s4x_macled_info;

mac_led_api_para_t e530_48s4x_mac_led_default_entry[E530_48S4X_LED_MAC_NUM] =
{
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
      .port_id = 61,
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
      .port_id = 63,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 62,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
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
      .port_id = 45,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 47,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 46,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
};

led2mac_t e530_48s4x_led2mac[E530_48S4X_LED_MAC_NUM] =
{
    /* panel port 33-52 */
    {
      .sysfs = "/sys/class/leds/port33/brightness",
      .para  = {
                 .port_id = 25,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port34/brightness",
      .para  = {
                 .port_id = 24,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port35/brightness",
      .para  = {
                 .port_id = 27,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port36/brightness",
      .para  = {
                 .port_id = 26,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port37/brightness",
      .para  = {
                 .port_id = 13,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port38/brightness",
      .para  = {
                 .port_id = 12,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port39/brightness",
      .para  = {
                 .port_id = 15,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port40/brightness",
      .para  = {
                 .port_id = 14,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port41/brightness",
      .para  = {
                 .port_id = 29,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port42/brightness",
      .para  = {
                 .port_id = 28,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port43/brightness",
      .para  = {
                 .port_id = 31,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port44/brightness",
      .para  = {
                 .port_id = 30,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port45/brightness",
      .para  = {
                 .port_id = 61,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port46/brightness",
      .para  = {
                 .port_id = 60,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port47/brightness",
      .para  = {
                 .port_id = 63,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port48/brightness",
      .para  = {
                 .port_id = 62,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port49/brightness",
      .para  = {
                 .port_id = 44,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port50/brightness",
      .para  = {
                 .port_id = 45,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port51/brightness",
      .para  = {
                 .port_id = 47,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port52/brightness",
      .para  = {
                 .port_id = 46,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
};

mac_led_api_para_t e530_48s4x_v2_mac_led_default_entry[E530_48S4X_V2_LED_MAC_NUM] =
{
    {
      .port_id = 0,
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
      .port_id = 2,
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
      .port_id = 4,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 5,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 6,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 7,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },

    {
      .port_id = 16,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 17,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 18,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 19,
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
      .port_id = 21,
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
      .port_id = 23,
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
      .port_id = 9,
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
      .port_id = 11,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },

    {
      .port_id = 32,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 33,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 34,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 35,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },

    {
      .port_id = 36,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 37,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 38,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 39,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },

    {
      .port_id = 40,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 41,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 42,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 43,
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
      .port_id = 61,
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
      .port_id = 63,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 62,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
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
      .port_id = 45,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 47,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
    {
      .port_id = 46,
      .lchip   = 0,
      .ctl_id  = 0,
      .mode    = LED_MODE_2_FORCE_OFF,
      .fixed   = 0,
    },
};

led2mac_t e530_48s4x_v2_led2mac[E530_48S4X_V2_LED_MAC_NUM] =
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
                 .port_id = 4,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port6/brightness",
      .para  = {
                 .port_id = 5,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port7/brightness",
      .para  = {
                 .port_id = 6,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port8/brightness",
      .para  = {
                 .port_id = 7,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port9/brightness",
      .para  = {
                 .port_id = 16,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port10/brightness",
      .para  = {
                 .port_id = 17,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port11/brightness",
      .para  = {
                 .port_id = 18,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port12/brightness",
      .para  = {
                 .port_id = 19,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port13/brightness",
      .para  = {
                 .port_id = 20,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port14/brightness",
      .para  = {
                 .port_id = 21,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port15/brightness",
      .para  = {
                 .port_id = 22,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port16/brightness",
      .para  = {
                 .port_id = 23,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port17/brightness",
      .para  = {
                 .port_id = 8,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port18/brightness",
      .para  = {
                 .port_id = 9,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port19/brightness",
      .para  = {
                 .port_id = 10,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port20/brightness",
      .para  = {
                 .port_id = 11,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port21/brightness",
      .para  = {
                 .port_id = 32,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port22/brightness",
      .para  = {
                 .port_id = 33,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port23/brightness",
      .para  = {
                 .port_id = 34,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port24/brightness",
      .para  = {
                 .port_id = 35,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port25/brightness",
      .para  = {
                 .port_id = 36,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port26/brightness",
      .para  = {
                 .port_id = 37,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port27/brightness",
      .para  = {
                 .port_id = 38,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port28/brightness",
      .para  = {
                 .port_id = 39,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port29/brightness",
      .para  = {
                 .port_id = 40,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port30/brightness",
      .para  = {
                 .port_id = 41,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port31/brightness",
      .para  = {
                 .port_id = 42,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port32/brightness",
      .para  = {
                 .port_id = 43,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    /* panel port 33-52 */
    {
      .sysfs = "/sys/class/leds/port33/brightness",
      .para  = {
                 .port_id = 25,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port34/brightness",
      .para  = {
                 .port_id = 24,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port35/brightness",
      .para  = {
                 .port_id = 27,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port36/brightness",
      .para  = {
                 .port_id = 26,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port37/brightness",
      .para  = {
                 .port_id = 13,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port38/brightness",
      .para  = {
                 .port_id = 12,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port39/brightness",
      .para  = {
                 .port_id = 15,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port40/brightness",
      .para  = {
                 .port_id = 14,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port41/brightness",
      .para  = {
                 .port_id = 29,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port42/brightness",
      .para  = {
                 .port_id = 28,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port43/brightness",
      .para  = {
                 .port_id = 31,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port44/brightness",
      .para  = {
                 .port_id = 30,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port45/brightness",
      .para  = {
                 .port_id = 61,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port46/brightness",
      .para  = {
                 .port_id = 60,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port47/brightness",
      .para  = {
                 .port_id = 63,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port48/brightness",
      .para  = {
                 .port_id = 62,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },

    {
      .sysfs = "/sys/class/leds/port49/brightness",
      .para  = {
                 .port_id = 44,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port50/brightness",
      .para  = {
                 .port_id = 45,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port51/brightness",
      .para  = {
                 .port_id = 47,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
    {
      .sysfs = "/sys/class/leds/port52/brightness",
      .para  = {
                 .port_id = 46,
                 .lchip   = 0,
                 .ctl_id  = 0,
               },
    },
};

static ctc_chip_phy_mapping_para_t ctc_sai_e530_48s4x_phy_mapping_para;
phy_info_t ctc_sai_e530_48s4x_phy_info_tbl[] = {
    {
      .macid = 0,
      .busid = 1,
      .addr  = 0,
    },    /* Port 1 */
    {
      .macid = 1,
      .busid = 1,
      .addr  = 1,
    },    /* Port 2 */
    {
      .macid = 2,
      .busid = 1,
      .addr  = 2,
    },    /* Port 3 */
    {
      .macid = 3,
      .busid = 1,
      .addr  = 3,
    },    /* Port 4 */
    {
      .macid = 4,
      .busid = 1,
      .addr  = 4,
    },    /* Port 5 */
    {
      .macid = 5,
      .busid = 1,
      .addr  = 5,
    },    /* Port 6 */
    {
      .macid = 6,
      .busid = 1,
      .addr  = 6,
    },    /* Port 7 */
    {
      .macid = 7,
      .busid = 1,
      .addr  = 7,
    },    /* Port 8 */

    {
      .macid = 16,
      .busid = 2,
      .addr  = 0,
    },    /* Port 9 */
    {
      .macid = 17,
      .busid = 2,
      .addr  = 1,
    },    /* Port 10 */
    {
      .macid = 18,
      .busid = 2,
      .addr  = 2,
    },    /* Port 11 */
    {
      .macid = 19,
      .busid = 2,
      .addr  = 3,
    },    /* Port 12 */
    {
      .macid = 20,
      .busid = 2,
      .addr  = 4,
    },    /* Port 13 */
    {
      .macid = 21,
      .busid = 2,
      .addr  = 5,
    },    /* Port 14 */
    {
      .macid = 22,
      .busid = 2,
      .addr  = 6,
    },    /* Port 15 */
    {
      .macid = 23,
      .busid = 2,
      .addr  = 7,
    },    /* Port 16 */

    {
      .macid = 8,
      .busid = 3,
      .addr  = 0,
    },    /* Port 17 */
    {
      .macid = 9,
      .busid = 3,
      .addr  = 1,
    },    /* Port 18 */
    {
      .macid = 10,
      .busid = 3,
      .addr  = 2,
    },    /* Port 19 */
    {
      .macid = 11,
      .busid = 3,
      .addr  = 3,
    },    /* Port 20 */
    {
      .macid = 32,
      .busid = 3,
      .addr  = 4,
    },    /* Port 21 */
    {
      .macid = 33,
      .busid = 3,
      .addr  = 5,
    },    /* Port 22 */
    {
      .macid = 34,
      .busid = 3,
      .addr  = 6,
    },    /* Port 23 */
    {
      .macid = 35,
      .busid = 3,
      .addr  = 7,
    },    /* Port 24 */

    {
      .macid = 36,
      .busid = 0,
      .addr  = 0,
    },    /* Port 25 */
    {
      .macid = 37,
      .busid = 0,
      .addr  = 1,
    },    /* Port 26 */
    {
      .macid = 38,
      .busid = 0,
      .addr  = 2,
    },    /* Port 27 */
    {
      .macid = 39,
      .busid = 0,
      .addr  = 3,
    },    /* Port 28 */
    {
      .macid = 40,
      .busid = 0,
      .addr  = 4,
    },    /* Port 29 */
    {
      .macid = 41,
      .busid = 0,
      .addr  = 5
    },    /* Port 30 */
    {
      .macid = 42,
      .busid = 0,
      .addr  = 6,
    },    /* Port 31 */
    {
      .macid = 43,
      .busid = 0,
      .addr  = 7,
    },    /* Port 32 */
};


int32 ctc_sai_e530_48s4x_create_fiber_handle(glb_card_t *p_glb_card)
{
    int idx = 0;

    p_glb_card->fiber_num = E530_48S4X_FIBER_NUM;
    p_glb_card->fiber_info_table = e530_48s4x_fiber_table;

    for (idx = 0; idx < E530_48S4X_FIBER_NUM; idx++)
    {
        e530_48s4x_fiber_table[idx].fiber_hdl = fiber_create_handle(&(e530_48s4x_fiber_table[idx].fiber_gen));
    }

    return 0;
}

int32 ctc_sai_e530_48s4x_create_macled_handle(glb_card_t *p_glb_card)
{
    char buf[3] = {0};
    int fd = -1;
    char hw_ver = 0x20;

    fd = open("/dev/mtd2", O_RDONLY);
    if (fd < 0)
    {
        hw_ver = 0x20;
    }
    else
    {
        lseek(fd, 0x1011, SEEK_SET);
        read(fd, buf, 3);
        close(fd);
        hw_ver = buf[2];
    }

    if (hw_ver == 0x10)
    {
        p_glb_card->macled_info = &e530_48s4x_macled_info;

        p_glb_card->macled_info->macled_gen.mac_table_id = 0;
        p_glb_card->macled_info->macled_gen.p_mac_led_info = (mac_led_info_t *)mem_malloc(
                                                              MEM_SYSTEM_MODULE, sizeof(mac_led_info_t));
        p_glb_card->macled_info->macled_gen.p_mac_led_info->table_num = 1;
        p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_num = E530_48S4X_LED_MAC_NUM;
        p_glb_card->macled_info->macled_gen.p_mac_led_info->slice0_mac_num = E530_48S4X_LED_MAC_NUM;
        p_glb_card->macled_info->macled_gen.p_mac_led_info->polarity = 1;
        p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_led_api_para = (mac_led_api_para_t **)mem_malloc(
                                                                                MEM_SYSTEM_MODULE,
                                                                                sizeof(mac_led_api_para_t*) *
                                                                                p_glb_card->macled_info->macled_gen.p_mac_led_info->table_num);
        p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_led_api_para[0] = e530_48s4x_mac_led_default_entry;

        
        p_glb_card->macled_info->macled_hdl = macled_create_handle(&(p_glb_card->macled_info->macled_gen));


        if (p_glb_card->macled_info->macled_hdl != NULL)
            p_glb_card->macled_info->macled_hdl->init(p_glb_card->macled_info->macled_hdl);

        e530_48s4x_macled_info.led2mac = (led2mac_t *)mem_malloc(MEM_SYSTEM_MODULE, sizeof(led2mac_t) * E530_48S4X_LED_MAC_NUM);
        e530_48s4x_macled_info.led2mac_size = E530_48S4X_LED_MAC_NUM;
        sal_memcpy(p_glb_card->macled_info->led2mac, e530_48s4x_led2mac, sizeof(led2mac_t) * E530_48S4X_LED_MAC_NUM);
    }
    else
    {
        p_glb_card->macled_info = &e530_48s4x_macled_info;

        p_glb_card->macled_info->macled_gen.mac_table_id = 0;
        p_glb_card->macled_info->macled_gen.p_mac_led_info = (mac_led_info_t *)mem_malloc(
                                                              MEM_SYSTEM_MODULE, sizeof(mac_led_info_t));
        p_glb_card->macled_info->macled_gen.p_mac_led_info->table_num = 1;
        p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_num = E530_48S4X_V2_LED_MAC_NUM;
        p_glb_card->macled_info->macled_gen.p_mac_led_info->slice0_mac_num = E530_48S4X_V2_LED_MAC_NUM;
        p_glb_card->macled_info->macled_gen.p_mac_led_info->polarity = 1;
        p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_led_api_para = (mac_led_api_para_t **)mem_malloc(
                                                                                MEM_SYSTEM_MODULE,
                                                                                sizeof(mac_led_api_para_t*) *
                                                                                p_glb_card->macled_info->macled_gen.p_mac_led_info->table_num);
        p_glb_card->macled_info->macled_gen.p_mac_led_info->mac_led_api_para[0] = e530_48s4x_v2_mac_led_default_entry;

        
        p_glb_card->macled_info->macled_hdl = macled_create_handle(&(p_glb_card->macled_info->macled_gen));


        if (p_glb_card->macled_info->macled_hdl != NULL)
            p_glb_card->macled_info->macled_hdl->init(p_glb_card->macled_info->macled_hdl);

        e530_48s4x_macled_info.led2mac = (led2mac_t *)mem_malloc(MEM_SYSTEM_MODULE, sizeof(led2mac_t) * E530_48S4X_V2_LED_MAC_NUM);
        e530_48s4x_macled_info.led2mac_size = E530_48S4X_V2_LED_MAC_NUM;
        sal_memcpy(p_glb_card->macled_info->led2mac, e530_48s4x_v2_led2mac, sizeof(led2mac_t) * E530_48S4X_V2_LED_MAC_NUM);
    }
    
    return 0;
}

int32 ctc_sai_e530_48s4x_phy_init(glb_card_t *p_glb_card)
{
    ctc_global_panel_ports_t phy_ports;
    uint8 loop = 0;
    uint32 gport = 0;
    uint8 gchip = 0;

    //SAI Mark, TODO, need phy_drv lib
    //extern int32 ctc_app_phy_init(uint8 lchip);
    //ctc_app_phy_init(0);

    sal_memset(&ctc_sai_e530_48s4x_phy_mapping_para, 0xff, sizeof(ctc_chip_phy_mapping_para_t));
    for (loop = 0; loop < sizeof(ctc_sai_e530_48s4x_phy_info_tbl)/sizeof(phy_info_t); loop++)
    {
        ctc_sai_e530_48s4x_phy_mapping_para.port_mdio_mapping_tbl[ctc_sai_e530_48s4x_phy_info_tbl[loop].macid] = ctc_sai_e530_48s4x_phy_info_tbl[loop].busid;
        ctc_sai_e530_48s4x_phy_mapping_para.port_phy_mapping_tbl[ctc_sai_e530_48s4x_phy_info_tbl[loop].macid] = ctc_sai_e530_48s4x_phy_info_tbl[loop].addr;
    }
    ctcs_chip_set_phy_mapping(0, &ctc_sai_e530_48s4x_phy_mapping_para);

    
    sal_memset(&phy_ports, 0, sizeof(phy_ports));
    ctcs_global_ctl_get(0, CTC_GLOBAL_PANEL_PORTS, (void*)&phy_ports);
    for (loop = 0; loop < phy_ports.count; loop++)
    {
        ctcs_get_gchip_id(0, &gchip);
        gport = CTC_MAP_LPORT_TO_GPORT(gchip, phy_ports.lport[loop]);
        ctcs_port_set_property(0, gport, CTC_PORT_PROP_PHY_INIT, 1);
    }
    for (loop = 0; loop < phy_ports.count; loop++)
    {
        ctcs_get_gchip_id(0, &gchip);
        gport = CTC_MAP_LPORT_TO_GPORT(gchip, phy_ports.lport[loop]);
        ctcs_port_set_port_en(0, gport, 0);
    }

    return 0;
}

void ctc_sai_e530_48s4x_platform_callback(void)
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

int32 ctc_sai_e530_48s4x_board_init(glb_card_t *p_glb_card)
{
    int ret = 0;

    ret += ctc_sai_e530_48s4x_create_fiber_handle(p_glb_card);
    ret += ctc_sai_e530_48s4x_create_macled_handle(p_glb_card);
    ret += ctc_sai_e530_48s4x_phy_init(p_glb_card);
    p_glb_card->platform_callback = ctc_sai_e530_48s4x_platform_callback;

    return ret;
}
