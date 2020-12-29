
/^typedef enum _sai_object_type_t/ {

    def_object = 1;
}


/^[ \t]*SAI_OBJECT_/ && def_object == 1 {

    def_object_item[object_type_num] = $1;
    
    object_type_num++;
}

/^} sai_object_type_t;/ {

    print  "ctc_sai_object_type_info_t* ctc_sai_metadata_all_object_type_infos[] = ";
    print  "{";
    print  "    NULL,";
    for (i = 1; i < (object_type_num-1); i++)
    {
        printf("    &ctc_sai_metadata_object_type_info_%s,\n", tolower(def_object_item[i])); 
    }
    print  "    NULL";
    print  "};\n"

    print  "ctc_sai_attr_metadata_t* ctc_sai_metadata_object_type_sai_null_attr_t[] = {";
    print  "    NULL";
    print  "};";

    print  "ctc_sai_attr_metadata_t** ctc_sai_metadata_attr_by_object_type[] = {";
    print  "    ctc_sai_metadata_object_type_sai_null_attr_t,";
    for (i = 1; i < (object_type_num-1); i++)
    {
        object_name = tolower(def_object_item[i]);
        sub(/^sai_object_type_/, "", object_name);
        printf("    ctc_sai_metadata_object_type_sai_%s_attr_t,\n", object_name);
    }
    print  "    NULL";
    print  "};\n";

    def_object = 0;
}

BEGIN{
    object_type_num = 0;
}
