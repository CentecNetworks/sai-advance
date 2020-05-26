#include "ctc_error.h"
#include "ctc_macro.h"
#include "ctc_sai_app_cfg_datapath_profile.h"
#include "ctc_sai_app_cfg_parse.h"

/*--------------------------------Define--------------------------------------*/

int32
ctc_app_read_datapath_profile_security_status(ctc_app_parse_file_t* pfile, ctc_datapath_global_cfg_t* p_datapath_cfg)
{
    uint8  entry_num = 0;
    int32  value = 0;
    const char* field_sub = NULL;

    /* get wlan enable*/
    entry_num = 1;
    ctc_app_parse_file(pfile,
                   "WLAN_ENABLE",
                   field_sub,
                   &value,
                   &entry_num);
    p_datapath_cfg->wlan_enable = value;

    /* get dot1ae enable*/
    entry_num = 1;
    ctc_app_parse_file(pfile,
                   "DOT1AE_ENABLE",
                   field_sub,
                   &value,
                   &entry_num);
    p_datapath_cfg->dot1ae_enable = value;
    return CTC_E_NONE;
}


int32
ctc_app_read_datapath_profile_pll_info(ctc_app_parse_file_t* pfile, ctc_datapath_global_cfg_t* p_datapath_cfg)
{
    uint8  entry_num = 0;
    int32  value = 0;
    const char* field_sub = NULL;

    /* get PLLA core frequency*/
    entry_num = 1;
    ctc_app_parse_file(pfile,
                   "CORE_PLLA",
                   field_sub,
                   &value,
                   &entry_num);
    p_datapath_cfg->core_frequency_a = value;

    /* get PLLB core frequency*/
    entry_num = 1;
    ctc_app_parse_file(pfile,
                   "CORE_PLLB",
                   field_sub,
                   &value,
                   &entry_num);
    p_datapath_cfg->core_frequency_b = value;

    return CTC_E_NONE;
}

int32
ctc_app_read_datapath_profile_serdes_info(ctc_app_parse_file_t* pfile, ctc_datapath_global_cfg_t* p_datapath_cfg)
{
    uint8    entry_num = CTC_DATAPATH_SERDES_NUM;
    uint8    cnt = 0;
    static uint32   rx_polarity[CTC_DATAPATH_SERDES_NUM] = {0};
    static uint32   tx_polarity[CTC_DATAPATH_SERDES_NUM] = {0};
    static uint32   is_dynamic[CTC_DATAPATH_SERDES_NUM] = {0};
    static uint32   serdes_mode[CTC_DATAPATH_SERDES_NUM] = {0};
    static uint32   serdes_id[CTC_DATAPATH_SERDES_NUM] = {0} ;
    static uint32   serdes_group[CTC_DATAPATH_SERDES_NUM] = {0} ;
    int      ret = 0;

    entry_num = CTC_DATAPATH_SERDES_NUM;
    ret = ctc_app_parse_file(pfile,
                       "SERDES_ITEM",
                       "SERDES_ID",
                       serdes_id,
                       &entry_num);

    ret = ctc_app_parse_file(pfile,
                       "SERDES_ITEM",
                       "SERDES_MODE",
                       serdes_mode,
                       &entry_num);

    ret = ctc_app_parse_file(pfile,
                       "SERDES_ITEM",
                       "SERDES_RX_POLY",
                       rx_polarity,
                       &entry_num);

    ret = ctc_app_parse_file(pfile,
                       "SERDES_ITEM",
                       "SERDES_TX_POLY",
                       tx_polarity,
                       &entry_num);

    ret = ctc_app_parse_file(pfile,
                       "SERDES_ITEM",
                       "SERDES_SWITCH",
                       is_dynamic,
                       &entry_num);

    ret = ctc_app_parse_file(pfile,
                       "SERDES_ITEM",
                       "SERDES_GROUP",
                       serdes_group,
                       &entry_num);

    for(cnt = 0; cnt < CTC_DATAPATH_SERDES_NUM; cnt++)
    {
        p_datapath_cfg->serdes[cnt].mode = serdes_mode[cnt];
        p_datapath_cfg->serdes[cnt].rx_polarity = rx_polarity[cnt];
        p_datapath_cfg->serdes[cnt].tx_polarity = tx_polarity[cnt];
        p_datapath_cfg->serdes[cnt].is_dynamic= is_dynamic[cnt];
        p_datapath_cfg->serdes[cnt].group = serdes_group[cnt];
    }

    return ret;
}

int32
ctc_app_get_datapath_profile(uint8* file_name, ctc_datapath_global_cfg_t* p_datapath_cfg)
{
    int32   ret;
    ctc_app_parse_file_t file;

    CTC_PTR_VALID_CHECK(file_name);
    CTC_PTR_VALID_CHECK(p_datapath_cfg);

    ret = ctc_app_parse_open_file((const char*)file_name, &file);
    if (ret != CTC_E_NONE)
    {
        return ret;
    }


    ctc_app_read_datapath_profile_security_status(&file, p_datapath_cfg);


    ctc_app_read_datapath_profile_pll_info(&file, p_datapath_cfg);

    ctc_app_read_datapath_profile_serdes_info(&file, p_datapath_cfg);

    ctc_app_parse_close_file(&file);

    return CTC_E_NONE;
}
