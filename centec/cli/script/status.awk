
/^#define SAI_STATUS/ && /L[\)]?$/ {

    def_enum_item[def_enum_num] = $2;
    def_enum_num++;
}

BEGIN {

    def_enum_type="sai_status_t"
    def_enum_num = 0;
}

END {

    for (i = 0; i < def_enum_num; i++)
    {
        printf("%s ctc_sai_metadata_%s_enum_values[] = \n",  def_enum_type, def_enum_type);
        printf("{\n");
        for (i = 0; i < def_enum_num; i++)
        {
            printf("    %s,\n",          def_enum_item[i]);
        }
        printf("    -1\n",          def_enum_item[i]);
        printf("};\n\n");

        printf("char* ctc_sai_metadata_%s_enum_values_names[] = \n",  def_enum_type);
        printf("{\n");
        for (i = 0; i < def_enum_num; i++)
        {
            printf("    \"%s\",\n",          def_enum_item[i]);
        }
        printf("    NULL\n",          def_enum_item[i]);
        printf("};\n\n");

        printf("ctc_sai_enum_metadata_t ctc_sai_metadata_enum_%s = \n",  def_enum_type);
        printf("{\n");
        printf("    .name                       = \"%s\",\n",            def_enum_type);
        printf("    .valuescount                = %u,\n",                def_enum_num);
        printf("    .values                     = %s_%s_%s,\n",         "(int*)ctc_sai_metadata", def_enum_type, "enum_values");
        printf("    .valuesnames                = %s_%s_%s,\n",         "ctc_sai_metadata", def_enum_type, "enum_values_names");
        print "};\n"
    }
}
