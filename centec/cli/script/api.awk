
/^typedef struct _sai_[0-9a-z_]+_api_t/ {

    api = $3;
    sub(/^_sai_/,   "", api);
    sub(/_api_t$/,  "", api);

    for (i = 0; i < def_obj_num; i++)
    {
        def_obj_name = def_obj_list[i]

        is_obj = 1;
        for (j = 0; j < def_ods_num; j++)
        {
            def_ods_name = def_ods_list[j]
            if (def_obj_name ~ def_ods_name && def_ods_name ~ def_obj_name)
            {
                is_obj = 0;
            }
        }

        if (i == 0)
        {
            printf("%-20s %-30s %u\n", api, def_obj_list[i], is_obj);
        }
        else
        {
            printf("%-20s %-30s %u\n", "",  def_obj_list[i], is_obj);
        }
    }
}

/^typedef struct/ && /entry_t$/ {

    def_ods_name = $3
    sub(/^_sai_/, "", def_ods_name);
    sub(/_t$/,    "", def_ods_name);
    
    def_ods_list[def_ods_num] = def_ods_name;
    def_ods_num++;
}

/^typedef enum/ && /attr_t$/ {

    def_obj_list[def_obj_num] = $3;

    sub(/^_sai_/,   "", def_obj_list[def_obj_num]);
    sub(/_attr_t$/, "", def_obj_list[def_obj_num]);

    def_obj_num++;
}

BEGIN {
    def_ods_num = 0;
    def_obj_num = 0;
}
