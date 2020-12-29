/**
 @file ctc_app_cfg.c

 @author  Copyright (C) 2011 Centec Networks Inc.  All rights reserved.

 @date 2010-7-5

 @version v2.0

 This file contains chip profile related function.
*/

/***************************************************************
 *
 * Header Files
 *
 ***************************************************************/
#include "sal.h"
#include "api/include/ctc_api.h"
#include "ctc_app.h"
#include "ctc_sai_app_cfg_chip_profile.h"
#include "ctc_sai_app_cfg_ftm_profile.h"
#include "ctc_sai_app_cfg_datapath_profile.h"
#include "sai.h"
#include "ctc_sai.h"

/***************************************************************
 *
 *  Defines and Macros
 *
 ***************************************************************/

#define MEM_CONFIG_PROFILE          "./mem_profile.cfg"
#define CTC_CHIP_CONFIG             "./chip_profile.cfg"
#define CTC_PHY_MAP                 "./phy_mapping.cfg"
#define CTC_DATAPATH_CONFIG         "./datapath_cfg.txt"
#define CTC_RESRC_CONFIG            "./resrc_profile.cfg"

#define MAX_EXTERNAL_NHNUM          16384
#define ACL_REDIRECT_FWD_PTR_NUM    1024
#define CTC_APP_MPLS_TBL_BLOCK_SIZE 64

#define COUNTOF(_array_)    ((uint32)(sizeof((_array_)) / sizeof((_array_)[0])))

/*
default interrupt configuration provide two types interrupt confuguration: msi and pin
    for pin interrupt:
         using ctc_intr_config for interrupt mapping to group
         using ctc_intr_group_config for register interrupt, default using 2 interrupt pin
    for msi interrupt:
         using ctc_intr_config_msi for interrupt mapping to group
         using ctc_intr_group_config_msi for register interrupt, now only support 1 msi interrupt
*/
#define __PIN_INTERRUPT_CONFIG__

ctc_intr_mapping_t ctc_app_intr_config[] =
{
    {0,    CTC_INTR_CHIP_FATAL                 },
    {0,    CTC_INTR_CHIP_NORMAL                },
    {INVG,  CTC_INTR_FUNC_PTP_TS_CAPTURE        },
    {0,  CTC_INTR_FUNC_PTP_MAC_TX_TS_CAPTURE },
    {0,  CTC_INTR_FUNC_PTP_TOD_PULSE_IN      },
    {0,  CTC_INTR_FUNC_PTP_TOD_CODE_IN_RDY   },
    {INVG,  CTC_INTR_FUNC_PTP_SYNC_PULSE_IN     },
    {INVG,  CTC_INTR_FUNC_PTP_SYNC_CODE_IN_RDY  },
    {0,       CTC_INTR_FUNC_OAM_DEFECT_CACHE      },
    {0,  CTC_INTR_FUNC_MDIO_CHANGE           },
    {0,    CTC_INTR_FUNC_MDIO_1G_CHANGE        },
    {0,    CTC_INTR_DMA_NORMAL                 },
    {0,      CTC_INTR_FUNC_LINK_CHAGNE       },
    {0,      CTC_INTR_FUNC_LINKAGG_FAILOVER      },
    {0,      CTC_INTR_FUNC_IPE_LEARN_CACHE       },
    {0,      CTC_INTR_FUNC_IPE_AGING_FIFO        },
    {0,      CTC_INTR_FUNC_STATS_FIFO            },
    {INVG, CTC_INTR_FUNC_APS_FAILOVER          },
    {0,      CTC_INTR_DMA_FUNC                   },
    {0,      CTC_INTR_FUNC_IPFIX_OVERFLOW},
};

ctc_intr_mapping_t ctc_app_intr_config_msi[] =
{
    {0,    CTC_INTR_CHIP_FATAL                 },
    {0,    CTC_INTR_CHIP_NORMAL                },
    {INVG,  CTC_INTR_FUNC_PTP_TS_CAPTURE        },
    {0,  CTC_INTR_FUNC_PTP_MAC_TX_TS_CAPTURE },
    {0,  CTC_INTR_FUNC_PTP_TOD_PULSE_IN      },
    {0,  CTC_INTR_FUNC_PTP_TOD_CODE_IN_RDY   },
    {INVG,  CTC_INTR_FUNC_PTP_SYNC_PULSE_IN     },
    {INVG,  CTC_INTR_FUNC_PTP_SYNC_CODE_IN_RDY  },
    {0,       CTC_INTR_FUNC_OAM_DEFECT_CACHE      },
    {0,  CTC_INTR_FUNC_MDIO_CHANGE           },
    {0,    CTC_INTR_FUNC_MDIO_1G_CHANGE        },
    {0,    CTC_INTR_DMA_NORMAL                 },
    {0,      CTC_INTR_FUNC_LINK_CHAGNE       },
    {0,      CTC_INTR_FUNC_LINKAGG_FAILOVER      },
    {0,      CTC_INTR_FUNC_IPE_LEARN_CACHE       },
    {0,      CTC_INTR_FUNC_IPE_AGING_FIFO        },
    {0, CTC_INTR_FUNC_STATS_FIFO            },
    {INVG, CTC_INTR_FUNC_APS_FAILOVER          },
    {0,      CTC_INTR_DMA_FUNC                   },
    {0,      CTC_INTR_FUNC_IPFIX_OVERFLOW},
};

/* default interrupt group configuration, need to change the IRQ and priority of groups based on your requirement
 * the priority range is [1, 139] for linux, thereinto [1, 99] is realtime schedule; and [0, 255] for vxworks
 */
ctc_intr_group_t ctc_app_intr_group_config[] =
{
    {0, 69, SAL_TASK_PRIO_DEF,  "other interrupt group"},
};

/* default interrupt group configuration, need to change the IRQ and priority of groups based on your requirement
 * the priority range is [1, 139] for linux, thereinto [1, 99] is realtime schedule; and [0, 255] for vxworks
 */
ctc_intr_group_t ctc_app_intr_group_config_msi[] =
{
    {0, 0, SAL_TASK_PRIO_DEF,  "msi interrupt group"},
};


/**
 @brief get interrupt configuration
*/

static int32
_ctc_app_get_intr_cfg(ctc_intr_global_cfg_t* p_intr_cfg, ctc_init_chip_info_t* p_chip_info)
{
    uint32 group_count = 0;
    uint32 intr_count = 0;
    uint8 interrupt_mode = p_chip_info->interrupt_mode;
    uint32 irq = p_chip_info->irq;

    /* use default global configuration in sys */
    group_count = interrupt_mode?(COUNTOF(ctc_app_intr_group_config_msi)):(COUNTOF(ctc_app_intr_group_config));
    intr_count = COUNTOF(ctc_app_intr_config);
    if ((group_count > CTC_INTR_MAX_GROUP) || (group_count > CTC_INTR_MAX_GROUP))
    {
        return CTC_E_INVALID_PARAM;
    }

    if ((intr_count > CTC_INTR_MAX_INTR) || (intr_count > CTC_INTR_MAX_INTR))
    {
        return CTC_E_INVALID_PARAM;
    }

    if (interrupt_mode == 1)
    {
        p_intr_cfg->group_count = group_count;
        p_intr_cfg->intr_count = intr_count;
        p_intr_cfg->p_group = ctc_app_intr_group_config_msi;
        p_intr_cfg->p_intr = ctc_app_intr_config_msi;
    }
    else
    {
        p_intr_cfg->group_count = group_count;
        p_intr_cfg->intr_count = intr_count;
        p_intr_cfg->p_group = ctc_app_intr_group_config;
        if (irq)
        {
            /*default use irq from ctc_app_intr_group_config*/
            p_intr_cfg->p_group->irq = irq;
        }
        p_intr_cfg->p_intr = ctc_app_intr_config;
    }
    p_intr_cfg->intr_mode = interrupt_mode;
    return CTC_E_NONE;
}


static int32
_ctc_app_get_dma_cfg(ctc_dma_global_cfg_t* p_dma_cfg)
{
    CTC_PTR_VALID_CHECK(p_dma_cfg);

    sal_memset(p_dma_cfg, 0, sizeof(ctc_dma_global_cfg_t));

#if defined (GREATBELT)
    p_dma_cfg->stats.desc_num          = 16;
    p_dma_cfg->stats.priority          = SAL_TASK_PRIO_DEF;
    p_dma_cfg->learning.desc_num       = (1024*4);
    p_dma_cfg->learning.priority       = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[0].desc_num      = 64;
    p_dma_cfg->pkt_rx[0].priority      = SAL_TASK_PRIO_NICE_HIGH;
    p_dma_cfg->pkt_rx[1].desc_num      = 64;
    p_dma_cfg->pkt_rx[1].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[2].desc_num      = 64;
    p_dma_cfg->pkt_rx[2].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[3].desc_num      = 64;
    p_dma_cfg->pkt_rx[3].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx_chan_num         = 4;
    p_dma_cfg->pkt_tx_desc_num         = 16;
    p_dma_cfg->table_r_desc_num        = 1;
    p_dma_cfg->table_w_desc_num        = 1;
    p_dma_cfg->pkt_rx_size_per_desc    = 256;
    p_dma_cfg->learning_proc_func      = NULL;
    p_dma_cfg->func_en_bitmap          = 0;
    p_dma_cfg->hw_learning_sync_en = 0;
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_PACKET_RX);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_PACKET_TX);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_TABLE_W);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_TABLE_R);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_HW_LEARNING);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_STATS);
#endif

#if defined (GOLDENGATE)
    p_dma_cfg->learning.desc_num   = 128;
    p_dma_cfg->learning.priority       = SAL_TASK_PRIO_DEF;
    p_dma_cfg->learning.dmasel       = 0;

    p_dma_cfg->ipfix.desc_num        = 64;
    p_dma_cfg->ipfix.priority            = SAL_TASK_PRIO_DEF;
    p_dma_cfg->ipfix.dmasel            = 0;

    /* must config 4 channel for dma packet rx TODO, channel number should get from cpureason module*/
    p_dma_cfg->pkt_rx_chan_num = 4;
    p_dma_cfg->pkt_rx[0].desc_num  = 1024;
    p_dma_cfg->pkt_rx[0].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[0].dmasel      = 0;
    p_dma_cfg->pkt_rx[0].data         = 256;
    p_dma_cfg->pkt_rx[1].desc_num  = 1024;
    p_dma_cfg->pkt_rx[1].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[1].dmasel      = 0;
    p_dma_cfg->pkt_rx[1].data         = 256;
    p_dma_cfg->pkt_rx[2].desc_num  = 1024;
    p_dma_cfg->pkt_rx[2].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[2].dmasel      = 0;
    p_dma_cfg->pkt_rx[2].data      = 256;
    p_dma_cfg->pkt_rx[3].desc_num      = 1024;
    p_dma_cfg->pkt_rx[3].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[3].dmasel      = 0;
    p_dma_cfg->pkt_rx[3].data      = 256;

    p_dma_cfg->pkt_tx.desc_num = 32;
    p_dma_cfg->pkt_tx.priority = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_tx.dmasel = 0;

    p_dma_cfg->func_en_bitmap          = 0;
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_PACKET_RX);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_PACKET_TX);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_HW_LEARNING);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_IPFIX);

    /*UML do not enable monitor and stats */
    if (0 == SDK_WORK_PLATFORM)
    {
        CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_MONITOR);
        CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_STATS);
    }
#endif

#if defined (DUET2) || defined (TSINGMA) || defined (TSINGMA_MX)
    p_dma_cfg->learning.desc_num   = 128;
    p_dma_cfg->learning.priority       = SAL_TASK_PRIO_DEF;
    p_dma_cfg->learning.dmasel       = 0;

    p_dma_cfg->ipfix.desc_num        = 64;
    p_dma_cfg->ipfix.priority            = SAL_TASK_PRIO_DEF;
    p_dma_cfg->ipfix.dmasel            = 0;

    /* must config 4 channel for dma packet rx TODO, channel number should get from cpureason module*/
    p_dma_cfg->pkt_rx_chan_num = 4;
    p_dma_cfg->pkt_rx[0].desc_num  = 1024;
    p_dma_cfg->pkt_rx[0].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[0].dmasel      = 0;
    p_dma_cfg->pkt_rx[0].data         = 256;
    p_dma_cfg->pkt_rx[1].desc_num  = 1024;
    p_dma_cfg->pkt_rx[1].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[1].dmasel      = 0;
    p_dma_cfg->pkt_rx[1].data         = 256;
    p_dma_cfg->pkt_rx[2].desc_num  = 1024;
    p_dma_cfg->pkt_rx[2].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[2].dmasel      = 0;
    p_dma_cfg->pkt_rx[2].data      = 256;
    p_dma_cfg->pkt_rx[3].desc_num      = 1024;
    p_dma_cfg->pkt_rx[3].priority      = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_rx[3].dmasel      = 0;
    p_dma_cfg->pkt_rx[3].data      = 256;
    p_dma_cfg->pkt_rx[3].pkt_knet_en = 0;

    p_dma_cfg->pkt_tx_ext[0].desc_num = 32;
    p_dma_cfg->pkt_tx_ext[0].priority = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_tx_ext[0].dmasel = 0;
    p_dma_cfg->pkt_tx_ext[1].desc_num = 32;
    p_dma_cfg->pkt_tx_ext[1].priority = SAL_TASK_PRIO_DEF;
    p_dma_cfg->pkt_tx_ext[1].dmasel = 0;
    p_dma_cfg->pkt_tx_ext[1].pkt_knet_en = 0;
    if (1 == SDK_WORK_PLATFORM)
    {
        p_dma_cfg->pkt_tx_ext[0].desc_num = 128;
        p_dma_cfg->pkt_tx_ext[1].desc_num = 128;
    }

    p_dma_cfg->func_en_bitmap          = 0;
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_PACKET_RX);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_PACKET_TX);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_HW_LEARNING);
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_IPFIX);

#if defined (DUET2) || defined (TSINGMA)
    CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_SDC);
#endif

    /*UML do not enable monitor and stats */
    if (0 == SDK_WORK_PLATFORM)
    {
        CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_MONITOR);
        CTC_BIT_SET(p_dma_cfg->func_en_bitmap, CTC_DMA_FUNC_STATS);
    }
#endif


    return CTC_E_NONE;
}

static int32
_ctc_app_get_profile(uint8 lchip, char* init_cfg, char* datapath_cfg, char* mem_cfg, ctc_init_cfg_t* p_init_config, ctc_init_chip_info_t* p_chip_info)
{
    int32 ret = 0;
    uint8 index = 0;

    /*read chip profile.cfg*/
    ret = ctc_app_get_chip_profile((uint8*)init_cfg, p_init_config, p_chip_info);
    if (ret < CTC_E_NONE)
    {
        CTC_SAI_LOG_ERROR(SAI_API_SWITCH, "Failed to get chip cfg \r\n");
        return ret;
    }

    ctc_app_set_phy_mapping((uint8*)CTC_PHY_MAP, p_init_config, p_chip_info);

    /*read ftm mem_profile.cfg*/
    ret = ctc_app_read_ftm_profile((int8*)mem_cfg, &(p_init_config->ftm_info));
    if (ret == CTC_E_NONE)
    {
        CTC_SAI_LOG_DEBUG(SAI_API_SWITCH, "Use user-defined profile to initialize FTM \n");
        p_init_config->ftm_info.profile_type = CTC_FTM_PROFILE_USER_DEFINE;
    }
    else
    {
        //default memory profile
        p_init_config->ftm_info.profile_type = p_chip_info->profile_type;
        if (p_init_config->ftm_info.profile_type == CTC_FTM_PROFILE_USER_DEFINE)
        {
            p_init_config->ftm_info.profile_type = CTC_FTM_PROFILE_0;
        }

    }

    /*read datapath_cfg.cfg*/
    ret = ctc_app_get_datapath_profile((uint8*)datapath_cfg, p_init_config->p_datapath_cfg);
    if (ret < 0)
    {
        if ((1 == SDK_WORK_PLATFORM) || ((0 == SDK_WORK_PLATFORM) && (1 == SDK_WORK_ENV)))
        {
            for (index = 0; index < CTC_DATAPATH_SERDES_NUM; index++)
            {
                p_init_config->p_datapath_cfg->serdes[index].mode = CTC_CHIP_SERDES_XFI_MODE;
            }

            p_init_config->p_datapath_cfg->core_frequency_a = 600;
            p_init_config->p_datapath_cfg->core_frequency_b = 500;
            p_init_config->p_datapath_cfg->wlan_enable = 1;
            p_init_config->p_datapath_cfg->dot1ae_enable = 1;
        }
    }

    /*read datapath_cfg.cfg*/
    //ret = ctc_app_get_resrc_profile((uint8*)CTC_RESRC_CONFIG, &p_init_config->p_qos_cfg->resrc_pool);
    //if (ret < 0)
    {
        sal_memset(&(p_init_config->p_qos_cfg->resrc_pool), 0, sizeof(ctc_qos_resrc_pool_cfg_t));
        //CTC_SAI_LOG_DEBUG(SAI_API_SWITCH, "Use default resrc profile \r\n");
    }


    return CTC_E_NONE;
}
/* Get sdk module init param*/

uint16
_ctc_app_mpls_init_helper(ctc_init_chip_info_t * chip_info, ctc_mpls_init_t* mpls_init)
{
    uint32 size_type = 0;
    uint32 size = 0;
    uint8  space_id = 0;

    for (space_id = 0; space_id < 4; space_id++)
    {
        mpls_init->space_info[space_id].enable = FALSE;
        size = chip_info->mpls_entry_num[space_id]/CTC_APP_MPLS_TBL_BLOCK_SIZE;
        size_type = 0;
        if (size)
        {
            while (size > 1)
            {
                size >>= 1;
                size_type++;
            }

            mpls_init->space_info[space_id].enable = TRUE;
            mpls_init->space_info[space_id].sizetype = size_type;
        }
    }
    return CTC_E_NONE;
}

/* SYSTEM MODIFIED by taocy for CirrusOS E530 ECMP, 20200514*/
#define CTC_SAI_DEFAULT_MAX_ECMP_NUM        64

static int32
_ctc_app_get_init_para(uint8 lchip, ctc_init_cfg_t * p_init_config, ctc_init_chip_info_t* p_chip_info)
{
    /*1. Get Nexthop module init parameter*/
    p_init_config->p_nh_cfg->max_external_nhid        = p_chip_info->ext_nexthop_num
        ? p_chip_info->ext_nexthop_num : MAX_EXTERNAL_NHNUM;
    p_init_config->p_nh_cfg->acl_redirect_fwd_ptr_num = ACL_REDIRECT_FWD_PTR_NUM;
    p_init_config->p_nh_cfg->max_ecmp                 = CTC_SAI_DEFAULT_MAX_ECMP_NUM; /* SYSTEM MODIFIED by taocy for CirrusOS E530 ECMP, increase from 16 to 64, 20200514*/
    p_init_config->p_nh_cfg->nh_edit_mode             = p_chip_info->nh_dedit_mode;
    p_init_config->p_nh_cfg->max_tunnel_id            = p_chip_info->mpls_tunnel_num
        ? p_chip_info->mpls_tunnel_num : CTC_NH_DEFAULT_MAX_MPLS_TUNNEL_NUM;

    p_init_config->p_nh_cfg->h_ecmp_en = p_chip_info->h_ecmp_en;

    /*2. Get Oam module init parameter*/
    p_init_config->p_oam_cfg->maid_len_format              = 3;
    p_init_config->p_oam_cfg->mep_index_alloc_by_sdk       = 1;
    p_init_config->p_oam_cfg->tp_section_oam_based_l3if    = 1; //SAI default use L3if
    p_init_config->p_oam_cfg->tp_y1731_ach_chan_type       = 0x8902;
    p_init_config->p_oam_cfg->mep_1ms_num                  = p_chip_info->bfd_mep_num
        ? p_chip_info->bfd_mep_num : 500;
    p_init_config->p_oam_cfg->tp_bfd_333ms                 = 0;
    p_init_config->p_oam_cfg->mpls_pw_vccv_with_ip_en      = p_chip_info->bfd_vccv_with_ip_en;
    p_init_config->p_oam_cfg->tp_csf_ach_chan_type         = 0x40;
    p_init_config->p_oam_cfg->tp_csf_clear                 = 0x0;
    p_init_config->p_oam_cfg->tp_csf_fdi                   = 0x1;
    p_init_config->p_oam_cfg->tp_csf_los                   = 0x7;
    p_init_config->p_oam_cfg->tp_csf_rdi                   = 0x2;

    /*3. Get Interrupt module init parameter*/
    _ctc_app_get_intr_cfg(p_init_config->p_intr_cfg, p_chip_info);

    /*4. Get Stats module init parameter*/
    p_init_config->p_stats_cfg->stats_bitmap     |= p_chip_info->stats_port_en ? CTC_STATS_PORT_STATS
                                                    : p_init_config->p_stats_cfg->stats_bitmap;
    p_init_config->p_stats_cfg->stats_bitmap     |= p_chip_info->stats_ecmp_en ? CTC_STATS_ECMP_STATS
                                                    : p_init_config->p_stats_cfg->stats_bitmap;
    p_init_config->p_stats_cfg->stats_bitmap     |= p_chip_info->stats_queue_deq_en ? CTC_STATS_QUEUE_DEQ_STATS
                                                    : p_init_config->p_stats_cfg->stats_bitmap;
    p_init_config->p_stats_cfg->stats_bitmap     |= p_chip_info->stats_queue_drop_en ? CTC_STATS_QUEUE_DROP_STATS
                                                    : p_init_config->p_stats_cfg->stats_bitmap;
    p_init_config->p_stats_cfg->stats_bitmap     |= p_chip_info->stats_flow_policer_en ? CTC_STATS_FLOW_POLICER_STATS
                                                    : p_init_config->p_stats_cfg->stats_bitmap;
    p_init_config->p_stats_cfg->stats_bitmap     |= p_chip_info->stats_vlan_en ? CTC_STATS_VLAN_STATS
                                                    : p_init_config->p_stats_cfg->stats_bitmap;
    p_init_config->p_stats_cfg->stats_bitmap     |= p_chip_info->stats_vrf_en ? CTC_STATS_VRF_STATS
                                                    : p_init_config->p_stats_cfg->stats_bitmap;
    p_init_config->p_stats_cfg->policer_stats_num = p_chip_info->stats_policer_num;

    /*5. Get Fdb module init parameter*/
    p_init_config->p_l2_fdb_cfg->flush_fdb_cnt_per_loop = 0;
    p_init_config->p_l2_fdb_cfg->default_entry_rsv_num  = p_chip_info->max_fid_num;
    p_init_config->p_l2_fdb_cfg->hw_learn_en            = p_chip_info->fdb_hw_learning_mode;
    p_init_config->p_l2_fdb_cfg->logic_port_num         = p_chip_info->logic_port_num;
    p_init_config->p_l2_fdb_cfg->stp_mode               = p_chip_info->stp_mode;
    p_init_config->p_l2_fdb_cfg->trie_sort_en           = p_chip_info->trie_sort_en;

    /*6. Get Mpls module init parameter*/
    _ctc_app_mpls_init_helper(p_chip_info, p_init_config->p_mpls_cfg);

    /*7. Get Dma module init parameter*/
    CTC_ERROR_RETURN(_ctc_app_get_dma_cfg(p_init_config->p_dma_cfg));
    p_init_config->p_dma_cfg->hw_learning_sync_en =
                            p_init_config->p_l2_fdb_cfg->hw_learn_en;/*for update neighbor when vlanif*/
    /*8. Get packet module init parameter*/

    /*9. Get bpe module init parameter*/
    p_init_config->p_bpe_cfg->is_port_extender = p_chip_info->bpe_br_pe_en;
    p_init_config->p_bpe_cfg->max_uc_ecid_id = p_chip_info->bpe_br_uc_max_ecid;
    p_init_config->p_bpe_cfg->max_mc_ecid_id = p_chip_info->bpe_br_mc_max_ecid;
    p_init_config->p_bpe_cfg->port_base = p_chip_info->bpe_br_port_base;

    /*10 Get chip config*/
    p_init_config->p_chip_cfg->cut_through_en       = ((0 != p_chip_info->cut_through_speed)?1:0);
    p_init_config->p_chip_cfg->cut_through_speed    = p_chip_info->cut_through_speed;
    if (p_chip_info->cut_through_speed > 3)
    {
        p_init_config->p_chip_cfg->cut_through_speed_bitmap = p_chip_info->cut_through_bitmap;
    }
    p_init_config->p_chip_cfg->alpm_affinity_mask = p_chip_info->alpm_affinity_mask;
    p_init_config->p_chip_cfg->normal_affinity_mask = p_chip_info->normal_affinity_mask;

    p_init_config->p_chip_cfg->ecc_recover_en       = p_chip_info->ecc_recover_en;
    p_init_config->p_chip_cfg->tcam_scan_en         = p_chip_info->tcam_scan_en;
    p_init_config->p_chip_cfg->sdb_en               = p_chip_info->sdb_en;
    p_init_config->p_chip_cfg->cpu_port_en = p_chip_info->cpu_port_en;
    p_init_config->p_chip_cfg->cpu_port = p_chip_info->cpu_port;
    p_init_config->p_chip_cfg->gb_gg_interconnect_en = p_chip_info->lag_gb_gg_interconnect_en;

    if (p_init_config->p_chip_cfg->cpu_port_en)
    {
        p_init_config->p_chip_cfg->cpu_mac_da[0][0] = 0xFE;
        p_init_config->p_chip_cfg->cpu_mac_da[0][1] = 0xFD;
        p_init_config->p_chip_cfg->cpu_mac_da[0][2] = 0x00;
        p_init_config->p_chip_cfg->cpu_mac_da[0][3] = 0x00;
        p_init_config->p_chip_cfg->cpu_mac_da[0][4] = 0x00;
        p_init_config->p_chip_cfg->cpu_mac_da[0][5] = 0x00;

        p_init_config->p_chip_cfg->cpu_mac_sa[0] = 0xFE;
        p_init_config->p_chip_cfg->cpu_mac_sa[1] = 0xFD;
        p_init_config->p_chip_cfg->cpu_mac_sa[2] = 0x00;
        p_init_config->p_chip_cfg->cpu_mac_sa[3] = 0x00;
        p_init_config->p_chip_cfg->cpu_mac_sa[4] = 0x00;
        p_init_config->p_chip_cfg->cpu_mac_sa[5] = 0x01;

        p_init_config->p_chip_cfg->tpid = 0x8100;
        p_init_config->p_chip_cfg->vlanid = 0x23;
    }

    /*11 Get qos config*/
    if (p_init_config->p_qos_cfg)
    {
        p_init_config->p_qos_cfg->policer_num = p_chip_info->policer_num
                                                ? p_chip_info->policer_num : 4096;
        p_init_config->p_qos_cfg->queue_num_per_network_port    = p_chip_info->queue_num_per_network_port
                                                                    ? p_chip_info->queue_num_per_network_port:16;
        p_init_config->p_qos_cfg->queue_num_for_cpu_reason      = p_chip_info->queue_num_for_cpu_reason
                                                                    ? p_chip_info->queue_num_for_cpu_reason : 128;
        p_init_config->p_qos_cfg->max_cos_level = 3;
        p_init_config->p_qos_cfg->cpu_queue_shape_profile_num   = p_chip_info->cpu_que_shp_profile_num;
        p_init_config->p_qos_cfg->ingress_vlan_policer_num   = p_chip_info->ingress_vlan_policer_num
                                                                     ? p_chip_info->ingress_vlan_policer_num : 0;
        p_init_config->p_qos_cfg->egress_vlan_policer_num   = p_chip_info->egress_vlan_policer_num
                                                                     ? p_chip_info->egress_vlan_policer_num : 0;
        p_init_config->p_qos_cfg->queue_num_per_internal_port   = p_chip_info->queue_num_per_internal_port
                                                                     ? p_chip_info->queue_num_per_internal_port : 0;
        p_init_config->p_qos_cfg->policer_merge_mode   = p_chip_info->policer_merge_mode
                                                                     ? p_chip_info->policer_merge_mode : 0;
        p_init_config->p_qos_cfg->policer_svc_mode             = p_chip_info->policer_svc_mode
                                                                     ? p_chip_info->policer_svc_mode : 0;
        p_init_config->p_qos_cfg->igs_macro_policer_num    = p_chip_info->igs_macro_policer_num
                                                                     ? p_chip_info->igs_macro_policer_num : 0;
        p_init_config->p_qos_cfg->egs_macro_policer_num     = p_chip_info->egs_macro_policer_num
                                                                     ? p_chip_info->egs_macro_policer_num : 0;
        p_init_config->p_qos_cfg->service_queue_mode   = p_chip_info->service_queue_mode
                                                                     ? p_chip_info->service_queue_mode : 0;
        p_init_config->p_qos_cfg->queue_num_per_ingress_service   = 4;

    }

    p_init_config->local_chip_num = p_chip_info->local_chip_num;
    sal_memcpy(p_init_config->gchip, p_chip_info->gchip, sizeof(uint8)*CTC_MAX_LOCAL_CHIP_NUM);

    /*12 Get stacking config*/
    p_init_config->p_stacking_cfg->hdr_glb.mac_da_chk_en     = 0;
    p_init_config->p_stacking_cfg->hdr_glb.ether_type_chk_en = 0;
    p_init_config->p_stacking_cfg->hdr_glb.vlan_tpid         = 0x8100;
    p_init_config->p_stacking_cfg->hdr_glb.ether_type        = 0x55bb;
    p_init_config->p_stacking_cfg->hdr_glb.ip_protocol       = 255;
    p_init_config->p_stacking_cfg->hdr_glb.udp_dest_port     = 0x1234;
    p_init_config->p_stacking_cfg->hdr_glb.udp_src_port      = 0x5678;
    p_init_config->p_stacking_cfg->hdr_glb.udp_en            = 0;
    p_init_config->p_stacking_cfg->hdr_glb.ip_ttl            = 255;
    p_init_config->p_stacking_cfg->hdr_glb.ip_dscp           = 63;
    p_init_config->p_stacking_cfg->hdr_glb.cos               = 7;
    p_init_config->p_stacking_cfg->hdr_glb.is_ipv4           = 1;
    p_init_config->p_stacking_cfg->hdr_glb.ipsa.ipv4         = 0x11223344;
    p_init_config->p_stacking_cfg->trunk_mode                 = p_chip_info->stacking_mode;
    p_init_config->p_stacking_cfg->fabric_mode               = p_chip_info->fabric_mode;

    p_init_config->p_stacking_cfg->version                   = p_chip_info->stacking_version;
    p_init_config->p_stacking_cfg->learning_mode = p_chip_info->stacking_learning_mode;

    p_init_config->p_stacking_cfg->connect_glb.member_num    = 1;
    p_init_config->p_stacking_cfg->connect_glb.mode          = 1;

    /*13 get module init flag*/
    p_init_config->init_flag = p_chip_info->init_flag;

    /* ptp default use inter clock*/
    p_init_config->p_ptp_cfg->ptp_ucast_en = 1;
    p_init_config->p_ptp_cfg->sync_copy_to_cpu_en = 0;
    p_init_config->p_ptp_cfg->signaling_copy_to_cpu_en = 0;
    p_init_config->p_ptp_cfg->management_copy_to_cpu_en = 0;
    p_init_config->p_ptp_cfg->delay_request_process_en = 1;
    p_init_config->p_ptp_cfg->port_based_ptp_en = 1;
    p_init_config->p_ptp_cfg->use_internal_clock_en = 1;
    p_init_config->p_ptp_cfg->cache_aging_time = 60;

    if (p_init_config->p_parser_cfg)
    {
        p_init_config->p_parser_cfg->ecmp_hash_type = 1;
        p_init_config->p_parser_cfg->linkagg_hash_type = 1;
        p_init_config->p_parser_cfg->lb_hash_mode = p_chip_info->lb_hash_mode ? p_chip_info->lb_hash_mode : 0;
    }
    return CTC_E_NONE;
}

int32
ctc_app_get_config(uint8 lchip, char* init_cfg, char* data_cfg, char* mem_cfg, ctc_init_cfg_t * p_init_config, ctc_init_cfg_t * user_init_config)
{
    ctc_init_chip_info_t chip_info;
    CTC_PTR_VALID_CHECK(p_init_config);

    sal_memset(&chip_info, 0, sizeof(ctc_init_chip_info_t));

    sal_memset(p_init_config->p_pkt_cfg, 0,  sizeof(ctc_pkt_global_cfg_t));
    sal_memset(p_init_config->p_nh_cfg, 0, sizeof(ctc_nh_global_cfg_t));
    sal_memset(p_init_config->p_oam_cfg, 0, sizeof(ctc_oam_global_t));
    sal_memset(p_init_config->p_l2_fdb_cfg, 0, sizeof(ctc_l2_fdb_global_cfg_t));
    sal_memset(p_init_config->p_mpls_cfg, 0, sizeof(ctc_mpls_init_t));
    sal_memset(p_init_config->p_intr_cfg, 0, sizeof(ctc_intr_global_cfg_t));
    sal_memset(p_init_config->p_dma_cfg, 0, sizeof(ctc_dma_global_cfg_t));
    sal_memset(p_init_config->ftm_info.key_info, 0, CTC_FTM_KEY_TYPE_MAX * sizeof(ctc_ftm_key_info_t));
    sal_memset(p_init_config->ftm_info.tbl_info, 0, CTC_FTM_TBL_TYPE_MAX * sizeof(ctc_ftm_tbl_info_t));
    sal_memset(p_init_config->p_bpe_cfg, 0, sizeof(ctc_bpe_global_cfg_t));
    sal_memset(p_init_config->p_chip_cfg, 0, sizeof(ctc_chip_global_cfg_t));
    sal_memset(p_init_config->p_datapath_cfg, 0, sizeof(ctc_datapath_global_cfg_t));
    sal_memset(p_init_config->p_qos_cfg, 0, sizeof(ctc_qos_global_cfg_t));
    sal_memset(p_init_config->p_ipuc_cfg, 0, sizeof(ctc_ipuc_global_cfg_t));
    sal_memset(p_init_config->p_stats_cfg, 0, sizeof(ctc_stats_global_cfg_t));
    sal_memset(p_init_config->p_stacking_cfg, 0, sizeof(ctc_stacking_glb_cfg_t));
    sal_memset(p_init_config->p_ptp_cfg, 0, sizeof(ctc_ptp_global_config_t));
    sal_memset(p_init_config->p_acl_cfg, 0, sizeof(ctc_acl_global_cfg_t));
    sal_memset(p_init_config->p_parser_cfg, 0, sizeof(ctc_parser_global_cfg_t));


    /*Get profile parameter*/
    CTC_ERROR_RETURN(_ctc_app_get_profile(lchip, init_cfg, data_cfg, mem_cfg, p_init_config, &chip_info));

    /*Get Module init parameter*/
    CTC_ERROR_RETURN(_ctc_app_get_init_para(lchip, p_init_config, &chip_info));
    if(user_init_config != NULL)
    {
        sal_memset(p_init_config, 0, sizeof(ctc_init_cfg_t));
        sal_memcpy(p_init_config, user_init_config, sizeof(ctc_init_cfg_t));
    }

    return CTC_E_NONE;
}
CTC_EXPORT_SYMBOL(ctc_app_get_config);

