
/^typedef struct/ && /entry_t$/ {

    def_ods_name = $3
    sub(/^_sai_/, "", def_ods_name);
    sub(/_t$/,    "", def_ods_name);
    
    def_ods_list[def_ods_num] = def_ods_name;
    def_ods_num++;
}

/^typedef enum/ && /attr_t$/ {

    attr_item_num = 0;
    def_attr_type = $3;
    def_attr = 1;
    enum_meta_data = "NULL"

    sub(/^_/, "", def_attr_type);

    def_obj_name = def_attr_type;
    sub(/^sai_/,    "", def_obj_name);
    sub(/_attr_t$/, "", def_obj_name);
    obj_list[def_obj_num] = def_obj_name;
    sai_def_obj_name      = def_obj_name;
    sai_def_obj_name      = toupper(sai_def_obj_name);
    def_obj_num++;

    sai_def_obj_name = "SAI_OBJECT_TYPE_" sai_def_obj_name;
}

/^[ \t]*\/\*\* @ignore/ && def_attr == 1 {
    attr_item_ignore = 1
}

/^[\t ]*SAI_/ && def_attr == 1 {

    if (attr_item_ignore == 0)
    {
        if ($1 !~ /START[,]?$/ && $1 !~ /END[,]?$/)
        {
            def_attr_item[attr_item_num] = $1
            sub(/,$/, "", def_attr_item[attr_item_num])

            printf("ctc_sai_attr_metadata_t ctc_sai_metadata_attr_%s = \n", tolower(def_attr_item[attr_item_num]));
            printf("{\n");
            printf("    .objecttype                    = %s,\n",                 sai_def_obj_name);
            printf("    .attrid                        = %s,\n",                 def_attr_item[attr_item_num]);
            printf("    .attridname                    = \"%s\",\n",             def_attr_item[attr_item_num]);
            printf("    .attrvaluetype                 = %s,\n",                 def_item_data[attr_item_num]);
            printf("    .isenum                        = %u,\n",                 is_enum);
            printf("    .isenumlist                    = %u,\n",                 is_enum_list);

            if (def_attr_item[attr_item_num] ~ /^SAI_ACL_ENTRY_ATTR_(USER_DEFINED_)?FIELD_[0-9A-Z_]+$/)
            {
                printf("    .isaclfield                    = 1,\n");
                printf("    .isaclaction                   = 0,\n");
            }
            else if (def_attr_item[attr_item_num] ~ /^SAI_ACL_ENTRY_ATTR_FIELD_[0-9A-Z_]+$/)
            {
                printf("    .isaclfield                    = 1,\n");
                printf("    .isaclaction                   = 0,\n");
            }
            else if (def_attr_item[attr_item_num] ~ /^SAI_ACL_ENTRY_ATTR_ACTION_[0-9A-Z_]+$/)
            {
                printf("    .isaclfield                    = 0,\n");
                printf("    .isaclaction                   = 1,\n");
            }
            else
            {
                printf("    .isaclfield                    = 0,\n");
                printf("    .isaclaction                   = 0,\n");
            }


            if (is_enum || is_enum_list)
            {
                printf("    .enummetadata                  = %s_%s,\n", "&ctc_sai_metadata_enum", def_enum_type);
            }
            else
            {
                printf("    .enummetadata                  = NULL\n");
            }

            printf("};\n\n");
            attr_item_num++

            if (def_attr_item[attr_item_num-1] == "SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_MIN")
            {
                for (i = 1; i < 255; i++)
                {
                    def_attr_item[attr_item_num] = "SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP_" i
                    printf("ctc_sai_attr_metadata_t ctc_sai_metadata_attr_%s_%u = \n", tolower("SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP"), i);
                    printf("{\n");
                    printf("    .objecttype                    = %s,\n",                 sai_def_obj_name);
                    printf("    .attrid                        = %s+%i,\n",              def_attr_item[attr_item_num-i], i);
                    printf("    .attridname                    = \"%s_%u\",\n",          "SAI_ACL_ENTRY_ATTR_USER_DEFINED_FIELD_GROUP", i);
                    printf("    .attrvaluetype                 = %s,\n",                 def_item_data[(attr_item_num-i)]);
                    printf("    .isenum                        = 0,\n");
                    printf("    .isenumlist                    = 0,\n");
                    printf("    .isaclfield                    = 1,\n");
                    printf("    .isaclaction                   = 0,\n");
                    printf("    .enummetadata                  = NULL\n");
                    printf("};\n\n");

                    attr_item_num++
                }
            }
        }
    }
    else
    {
        attr_item_ignore = 0;
    }

    is_enum_list = 0;
    is_enum = 0;
    def_enum_type = ""
}

/^[ ]*\* @type/ {

    if (NF == 3)
    {
        def_item_data[attr_item_num] = sai_attr_value_type[$3];
        if (def_item_data[attr_item_num] == "")
        {
            def_item_data[attr_item_num] = "CTC_SAI_ATTR_VALUE_TYPE_INT32";
            def_enum_type = $3;
            is_enum = 1;
        }
    }
    else if (NF == 4)
    {
        if ($3 == "sai_acl_field_data_t")
        {
            def_item_data[attr_item_num] = sai_attr_acl_filed_data_type[$4];
            if (def_item_data[attr_item_num] == "")
            {
                def_item_data[attr_item_num] = "CTC_SAI_ATTR_VALUE_TYPE_INT32";
            }
        }
        else if ($3 == "sai_acl_action_data_t")
        {
            def_item_data[attr_item_num] = sai_attr_acl_action_data_type[$4];
            if (def_item_data[attr_item_num] == "")
            {
                def_item_data[attr_item_num] = "CTC_SAI_ATTR_VALUE_TYPE_INT32";
            }
        }
        else
        {
            def_item_data[attr_item_num] = sai_attr_value_type[$3];
            is_enum_list = ($3 ~ /^sai_s32_list_t/) && ($4 ~ /sai_[0-9a-z_]+_t$/);
            def_enum_type = $4;
        }
    }
}

/^}/ && def_attr == 1 {

    printf("ctc_sai_attr_metadata_t* ctc_sai_metadata_object_type_%s[] = \n", def_attr_type);
    printf("{\n");
    for (i = 0; i < attr_item_num; i++)
    {
        printf("    &ctc_sai_metadata_attr_%s,\n", tolower(def_attr_item[i]));
    }
    print "    NULL"
    print "};\n"

    def_attr=0;
    attr_item_num = 0;
}

BEGIN{
    def_obj_num = 0;
    def_ods_num = 0;
    def_attr = 0;
    attr_item_num = 0;
    is_enum_list = 0;
    is_enum = 0;
    def_enum_type = ""

    sai_attr_value_type["bool"]                           = "CTC_SAI_ATTR_VALUE_TYPE_BOOL"                                                               
    sai_attr_value_type["char"]                           = "CTC_SAI_ATTR_VALUE_TYPE_CHARDATA"                                                           
    sai_attr_value_type["sai_uint8_t"]                    = "CTC_SAI_ATTR_VALUE_TYPE_UINT8"                                                              
    sai_attr_value_type["sai_int8_t"]                     = "CTC_SAI_ATTR_VALUE_TYPE_INT8"                                                               
    sai_attr_value_type["sai_uint16_t"]                   = "CTC_SAI_ATTR_VALUE_TYPE_UINT16"                                                             
    sai_attr_value_type["sai_int16_t"]                    = "CTC_SAI_ATTR_VALUE_TYPE_INT16"                                                              
    sai_attr_value_type["sai_uint32_t"]                   = "CTC_SAI_ATTR_VALUE_TYPE_UINT32"                                                             
    sai_attr_value_type["sai_int32_t"]                    = "CTC_SAI_ATTR_VALUE_TYPE_INT32"                                                              
    sai_attr_value_type["sai_uint64_t"]                   = "CTC_SAI_ATTR_VALUE_TYPE_UINT64"                                                             
    sai_attr_value_type["sai_int64_t"]                    = "CTC_SAI_ATTR_VALUE_TYPE_INT64"                                                              
    sai_attr_value_type["sai_pointer_t"]                  = "CTC_SAI_ATTR_VALUE_TYPE_POINTER"                                                            
    sai_attr_value_type["sai_mac_t"]                      = "CTC_SAI_ATTR_VALUE_TYPE_MAC"                                                                
    sai_attr_value_type["sai_ip4_t"]                      = "CTC_SAI_ATTR_VALUE_TYPE_IPV4"                                                               
    sai_attr_value_type["sai_ip6_t"]                      = "CTC_SAI_ATTR_VALUE_TYPE_IPV6"                                                               
    sai_attr_value_type["sai_ip_address_t"]               = "CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS"                                                         
    sai_attr_value_type["sai_ip_prefix_t"]                = "CTC_SAI_ATTR_VALUE_TYPE_IP_PREFIX"                                                          
    sai_attr_value_type["sai_object_id_t"]                = "CTC_SAI_ATTR_VALUE_TYPE_OBJECT_ID"                                                          
    sai_attr_value_type["sai_object_list_t"]              = "CTC_SAI_ATTR_VALUE_TYPE_OBJECT_LIST"                                                        
    sai_attr_value_type["sai_bool_list_t"]                = "CTC_SAI_ATTR_VALUE_TYPE_BOOL_LIST"                                                          
    sai_attr_value_type["sai_u8_list_t"]                  = "CTC_SAI_ATTR_VALUE_TYPE_UINT8_LIST"                                                         
    sai_attr_value_type["sai_s8_list_t"]                  = "CTC_SAI_ATTR_VALUE_TYPE_INT8_LIST"                                                          
    sai_attr_value_type["sai_u16_list_t"]                 = "CTC_SAI_ATTR_VALUE_TYPE_UINT16_LIST"                                                        
    sai_attr_value_type["sai_s16_list_t"]                 = "CTC_SAI_ATTR_VALUE_TYPE_INT16_LIST"                                                         
    sai_attr_value_type["sai_u32_list_t"]                 = "CTC_SAI_ATTR_VALUE_TYPE_UINT32_LIST"                                                        
    sai_attr_value_type["sai_s32_list_t"]                 = "CTC_SAI_ATTR_VALUE_TYPE_INT32_LIST"                                                         
    sai_attr_value_type["sai_u32_range_t"]                = "CTC_SAI_ATTR_VALUE_TYPE_UINT32_RANGE"                                                       
    sai_attr_value_type["sai_s32_range_t"]                = "CTC_SAI_ATTR_VALUE_TYPE_INT32_RANGE"                                                        
    sai_attr_value_type["sai_vlan_list_t"]                = "CTC_SAI_ATTR_VALUE_TYPE_VLAN_LIST"                                                          
    sai_attr_value_type["sai_qos_map_list_t"]             = "CTC_SAI_ATTR_VALUE_TYPE_QOS_MAP_LIST"                                                       
    sai_attr_value_type["sai_map_list_t"]                 = "CTC_SAI_ATTR_VALUE_TYPE_MAP_LIST"                                                           
    sai_attr_value_type["sai_acl_capability_t"]           = "CTC_SAI_ATTR_VALUE_TYPE_ACL_CAPABILITY"                                                     
    sai_attr_value_type["sai_acl_resource_list_t"]        = "CTC_SAI_ATTR_VALUE_TYPE_ACL_RESOURCE_LIST"                                                  
    sai_attr_value_type["sai_tlv_list_t"]                 = "CTC_SAI_ATTR_VALUE_TYPE_TLV_LIST"                                                           
    sai_attr_value_type["sai_segment_list_t"]             = "CTC_SAI_ATTR_VALUE_TYPE_SEGMENT_LIST"                                                       
    sai_attr_value_type["sai_ip_address_list_t"]          = "CTC_SAI_ATTR_VALUE_TYPE_IP_ADDRESS_LIST"                                                    
    sai_attr_value_type["sai_port_eye_values_list_t"]     = "CTC_SAI_ATTR_VALUE_TYPE_PORT_EYE_VALUES_LIST"                                               
    sai_attr_value_type["sai_timespec_t"]                 = "CTC_SAI_ATTR_VALUE_TYPE_TIMESPEC"                                                           
    sai_attr_value_type["sai_macsec_sak_t"]               = "CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SAK"                                                         
    sai_attr_value_type["sai_macsec_auth_key_t"]          = "CTC_SAI_ATTR_VALUE_TYPE_MACSEC_AUTH_KEY"                                                    
    sai_attr_value_type["sai_macsec_salt_t"]              = "CTC_SAI_ATTR_VALUE_TYPE_MACSEC_SALT"                                                        
    sai_attr_value_type["sai_system_port_config_t"]       = "CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG"                                                 
    sai_attr_value_type["sai_system_port_config_list_t"]  = "CTC_SAI_ATTR_VALUE_TYPE_SYSTEM_PORT_CONFIG_LIST"                                            
    sai_attr_value_type["sai_fabric_port_reachability_t"] = "CTC_SAI_ATTR_VALUE_TYPE_FABRIC_PORT_REACHABILITY"                                           
    sai_attr_value_type["sai_port_err_status_list_t"]     = "CTC_SAI_ATTR_VALUE_TYPE_PORT_ERR_STATUS_LIST"                                               
    sai_attr_value_type["sai_captured_timespec_t"]        = "CTC_SAI_ATTR_VALUE_TYPE_CAPTURED_TIMESPEC"                                                  
    sai_attr_value_type["sai_timeoffset_t"]               = "CTC_SAI_ATTR_VALUE_TYPE_TIMEOFFSET"                                                         
                                                                                                                                                  
    sai_attr_acl_filed_data_type["bool"]                  = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_BOOL"                                                
    sai_attr_acl_filed_data_type["sai_uint8_t"]           = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8"                                               
    sai_attr_acl_filed_data_type["sai_int8_t"]            = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT8"                                                
    sai_attr_acl_filed_data_type["sai_uint16_t"]          = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT16"                                              
    sai_attr_acl_filed_data_type["sai_int16_t"]           = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT16"                                               
    sai_attr_acl_filed_data_type["sai_uint32_t"]          = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT32"                                              
    sai_attr_acl_filed_data_type["sai_int32_t"]           = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_INT32"                                               
    sai_attr_acl_filed_data_type["sai_uint64_t"]          = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT64"                                              
    sai_attr_acl_filed_data_type["sai_mac_t"]             = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_MAC"                                                 
    sai_attr_acl_filed_data_type["sai_ip4_t"]             = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV4"                                                
    sai_attr_acl_filed_data_type["sai_ip6_t"]             = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_IPV6"                                                
    sai_attr_acl_filed_data_type["sai_object_id_t"]       = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_ID"                                           
    sai_attr_acl_filed_data_type["sai_object_list_t"]     = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_OBJECT_LIST"                                         
    sai_attr_acl_filed_data_type["sai_u8_list_t"]         = "CTC_SAI_ATTR_VALUE_TYPE_ACL_FIELD_DATA_UINT8_LIST"                                          
                                                                                                                                                   
    sai_attr_acl_action_data_type["bool"]                 = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_BOOL"                                               
    sai_attr_acl_action_data_type["sai_uint8_t"]          = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT8"                                              
    sai_attr_acl_action_data_type["sai_int8_t"]           = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT8"                                               
    sai_attr_acl_action_data_type["sai_uint16_t"]         = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT16"                                             
    sai_attr_acl_action_data_type["sai_int16_t"]          = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT16"                                              
    sai_attr_acl_action_data_type["sai_uint32_t"]         = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_UINT32"                                             
    sai_attr_acl_action_data_type["sai_int32_t"]          = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_INT32"                                              
    sai_attr_acl_action_data_type["sai_mac_t"]            = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_MAC"                                                
    sai_attr_acl_action_data_type["sai_ip4_t"]            = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IPV4"                                               
    sai_attr_acl_action_data_type["sai_ip6_t"]            = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IPV6"                                               
    sai_attr_acl_action_data_type["sai_object_id_t"]      = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_ID"                                          
    sai_attr_acl_action_data_type["sai_object_list_t"]    = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_OBJECT_LIST"                                        
    sai_attr_acl_action_data_type["sai_ip_address_t"]     = "CTC_SAI_ATTR_VALUE_TYPE_ACL_ACTION_DATA_IP_ADDRESS"
}

END {
    
    for (i = 0; i < def_obj_num; i++)
    {
        def_obj_name = "sai_object_type_" obj_list[i];
        
        printf("ctc_sai_object_type_info_t ctc_sai_metadata_object_type_info_%s = \n", def_obj_name);
        printf("{\n");
        printf("    .objecttype                 = %s,\n",                 toupper(def_obj_name));
        printf("    .objecttypename             = \"%s\",\n",             toupper(def_obj_name));

        is_obj = 1;
        for (j = 0; j < def_ods_num; j++)
        {
            def_ods_name = def_ods_list[j];
            def_obj_name = obj_list[i];

            if (def_obj_name ~ def_ods_name && def_ods_name ~ def_obj_name)
            {
                is_obj = 0;
            }
        }  
        printf("    .isobjectid                 = %d,\n",                 (is_obj == 1));
        printf("    .create                     = %s_%s,\n",              "ctc_sai_metadata_generic_create_sai_object_type", obj_list[i]);
        printf("    .remove                     = %s_%s,\n",              "ctc_sai_metadata_generic_remove_sai_object_type", obj_list[i]);
        printf("    .set                        = %s_%s,\n",              "ctc_sai_metadata_generic_set_sai_object_type", obj_list[i]);
        printf("    .get                        = %s_%s,\n",              "ctc_sai_metadata_generic_get_sai_object_type", obj_list[i]);
        printf("    .enummetadata               = %s_sai_%s_attr_t,\n",   "&ctc_sai_metadata_enum", obj_list[i]);
        printf("    .attrmetadata               = %s_sai_%s_attr_t,\n",   "ctc_sai_metadata_object_type", obj_list[i]);
        print "};\n"
    }
}
