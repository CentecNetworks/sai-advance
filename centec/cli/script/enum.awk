
/^#ifndef __SAIMETADATATYPES_H_/ {
    sai_meta_type = 1;
}

/^typedef enum/ {

    if ($3 !~ "_sai_attr_condition_type_t" && $3 !~ "_sai_default_value_type_t" && $3 !~ "_sai_attr_flags_t")
    {
        def_enum_num = 0;
        def_enum = 1;

        def_enum_type = $3;
        sub(/^_/, "", def_enum_type);
    }
}

/^[ \t]*\/\*\* @ignore/ && def_attr == 1 {
    attr_item_ignore = 1
}

/^[\t ]*SAI_/ && def_enum == 1 {

    if (attr_item_ignore == 0)
    {
        if ($1 !~ /START[,]?$/ && $1 !~ /END[,]?$/)
        {
            def_enum_item[def_enum_num] = $1
            sub(/,$/, "", def_enum_item[def_enum_num])

            def_enum_num++
        }
    }
    else
    {
        attr_item_ignore = 0;
    }
}

/^}/ && def_enum == 1 {

    if (def_enum_num != 0)
    {
        if (sai_meta_type == 1)
        {
            printf("ctc_%s ctc_sai_metadata_ctc_%s_enum_values[] = \n",  def_enum_type, def_enum_type);
        }
        else
        {
            printf("%s ctc_sai_metadata_%s_enum_values[] = \n",  def_enum_type, def_enum_type);
        }
        printf("{\n");
        for (i = 0; i < def_enum_num; i++)
        {
            if (sai_meta_type == 1)
            {
                printf("    CTC_%s,\n",          def_enum_item[i]);
            }
            else
            {
                printf("    %s,\n",          def_enum_item[i]);
            }
        }
        printf("    -1\n");
        printf("};\n\n");

        if (sai_meta_type == 1)
        {
            printf("char* ctc_sai_metadata_ctc_%s_enum_values_names[] = \n",  def_enum_type);
        }
        else
        {
            printf("char* ctc_sai_metadata_%s_enum_values_names[] = \n",  def_enum_type);
        }
        printf("{\n");
        for (i = 0; i < def_enum_num; i++)
        {
            if (sai_meta_type == 1)
            {
                printf("    \"CTC_%s\",\n",          def_enum_item[i]);
            }
            else
            {
                printf("    \"%s\",\n",          def_enum_item[i]);
            }
        }
        printf("    NULL\n");
        printf("};\n\n");

        if (sai_meta_type == 1)
        {
            printf("ctc_sai_enum_metadata_t ctc_sai_metadata_enum_ctc_%s = \n",  def_enum_type);
            printf("{\n");
            printf("    .name                       = \"ctc_%s\",\n",       def_enum_type);
            printf("    .valuescount                = %u,\n",               def_enum_num);
            printf("    .values                     = %s_ctc_%s_%s,\n",     "(int*)ctc_sai_metadata", def_enum_type, "enum_values");
            printf("    .valuesnames                = %s_ctc_%s_%s,\n",     "ctc_sai_metadata", def_enum_type, "enum_values_names");
        }
        else
        {
            printf("ctc_sai_enum_metadata_t ctc_sai_metadata_enum_%s = \n",  def_enum_type);
            printf("{\n");
            printf("    .name                       = \"%s\",\n",       def_enum_type);
            printf("    .valuescount                = %u,\n",           def_enum_num);
            printf("    .values                     = %s_%s_%s,\n",     "(int*)ctc_sai_metadata", def_enum_type, "enum_values");
            printf("    .valuesnames                = %s_%s_%s,\n",     "ctc_sai_metadata", def_enum_type, "enum_values_names");
        }
        print "};\n"
    }

    def_enum = 0
    def_enum_num = 0
}

BEGIN{
    #RS = "[ \t,]"
    sai_meta_type = 0;
}
