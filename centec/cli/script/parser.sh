#!/bin/bash

path=$1

if [ -z "$path" ]
then
    path=../../../
    dir=./
    temp=$dir
else
    dir=$path/centec/cli/src
    temp=$path/centec/cli/script
fi

if [ -e $dir/ctc_sai_meta_db.c ]
then
    rm $dir/ctc_sai_meta_db.c
fi

if [ -e $temp/obj2api.temp ]
then
    rm $temp/obj2api.temp
fi

echo "#include \"sai.h\""             >> $dir/ctc_sai_meta_db.c
echo "#include \"sal_types.h\""       >> $dir/ctc_sai_meta_db.c
echo "#include \"ctc_sai_meta_db.h\"" >> $dir/ctc_sai_meta_db.c
echo ""                               >> $dir/ctc_sai_meta_db.c

for sai_moduel_f in $(find $path/inc -type f -name '*.h' -type f ! -name 'sai.h' -type f ! -name 'saistatus.h' -type f ! -name 'saitypes.h' | sort )
do
    awk -f $path/centec/cli/script/api.awk  $sai_moduel_f >> $temp/obj2api.temp
done

awk -f $path/centec/cli/script/status.awk $path/inc/saistatus.h >> $dir/ctc_sai_meta_db.c

api_num=0
declare -a api_list

while read line
do
    if [[ ! -z $line ]]
    then
        n=$(echo $line | awk '{ print NF }')

        if [ "$n" -eq 3 ]
        then
            api=$(echo $line | awk '{ print $1 }')
            echo "sai_"$api"_api_t *sai_metadata_sai_"$api"_api = NULL;"  >> $dir/ctc_sai_meta_db.c
        fi
    fi
done < $temp/obj2api.temp

echo "" >> $dir/ctc_sai_meta_db.c

while read line
do
    if [[ ! -z $line ]]
    then
        n=$(echo $line | awk '{ print NF }')

        if [ "$n" -eq 3 ]
        then

            api=$(echo $line | awk '{ print $1 }')
            obj=$(echo $line | awk '{ print $2 }')
            is_obj=$(echo $line | awk '{ print $3 }')
            api_list[$api_num]=$api
            ((api_num++))
        elif [ "$n" -eq 2 ]
        then
            obj=$(echo $line | awk '{ print $1 }')
            is_obj=$(echo $line | awk '{ print $2 }')
        fi

        echo "sai_status_t ctc_sai_metadata_generic_create_sai_object_type_"$obj"(ctc_sai_object_meta_key_t *meta_key, sai_object_id_t switch_id, uint32_t attr_count, const sai_attribute_t *attr_list)"      >> $dir/ctc_sai_meta_db.c
        echo "{"                                                                                                                                                                                           >> $dir/ctc_sai_meta_db.c
        if [ "$is_obj" -eq 1 ]
        then
            if [ "$obj" == "switch" ]
            then
                echo "    return sai_metadata_sai_"$api"_api->create_"$obj"(&meta_key->objectkey.key.object_id, attr_count, attr_list);"                                                                   >> $dir/ctc_sai_meta_db.c
            else
                if [ "$obj" == "fdb_flush" ] ||  [ "$obj" == "hostif_packet" ]
                then
                    echo "    return SAI_STATUS_NOT_IMPLEMENTED;"                                                                                                                                          >> $dir/ctc_sai_meta_db.c
                else
                    echo "    return sai_metadata_sai_"$api"_api->create_"$obj"(&meta_key->objectkey.key.object_id, switch_id, attr_count, attr_list);"                                                    >> $dir/ctc_sai_meta_db.c
                fi
            fi
        else
            echo "    return sai_metadata_sai_"$api"_api->create_"$obj"(&meta_key->objectkey.key."$obj", attr_count, attr_list);"                                                                          >> $dir/ctc_sai_meta_db.c
        fi
        echo "};"                                                                                                                                                                                          >> $dir/ctc_sai_meta_db.c
        echo ""                                                                                                                                                                                            >> $dir/ctc_sai_meta_db.c

        echo "sai_status_t ctc_sai_metadata_generic_remove_sai_object_type_"$obj"(const ctc_sai_object_meta_key_t *meta_key)"                                                                                  >> $dir/ctc_sai_meta_db.c
        echo "{"                                                                                                                                                                                           >> $dir/ctc_sai_meta_db.c
        if [ "$is_obj" -eq 1 ]
        then
                if [ "$obj" == "fdb_flush" ] ||  [ "$obj" == "hostif_packet" ]
                then
                    echo "    return SAI_STATUS_NOT_IMPLEMENTED;"                                                                                                                                          >> $dir/ctc_sai_meta_db.c
                else
                    echo "    return sai_metadata_sai_"$api"_api->remove_"$obj"(meta_key->objectkey.key.object_id);"                                                                                       >> $dir/ctc_sai_meta_db.c
                fi
        else
            echo "    return sai_metadata_sai_"$api"_api->remove_"$obj"(&meta_key->objectkey.key."$obj");"                                                                                                 >> $dir/ctc_sai_meta_db.c
        fi
        echo "};"                                                                                                                                                                                          >> $dir/ctc_sai_meta_db.c
        echo ""                                                                                                                                                                                            >> $dir/ctc_sai_meta_db.c

        echo "sai_status_t ctc_sai_metadata_generic_set_sai_object_type_"$obj"(const ctc_sai_object_meta_key_t *meta_key, const sai_attribute_t *attr)"                                                        >> $dir/ctc_sai_meta_db.c
        echo "{"                                                                                                                                                                                           >> $dir/ctc_sai_meta_db.c
        if [ "$is_obj" -eq 1 ]
        then
            if [ "$obj" == "fdb_flush" ] ||  [ "$obj" == "hostif_packet" ]
            then
                echo "    return SAI_STATUS_NOT_IMPLEMENTED;"                                                                                                                                              >> $dir/ctc_sai_meta_db.c
            else
                echo "    return sai_metadata_sai_"$api"_api->set_"$obj"_attribute(meta_key->objectkey.key.object_id, attr);"                                                                              >> $dir/ctc_sai_meta_db.c
            fi
        else
            echo "    return sai_metadata_sai_"$api"_api->set_"$obj"_attribute(&meta_key->objectkey.key."$obj", attr);"                                                                                    >> $dir/ctc_sai_meta_db.c
        fi    
        echo "};"                                                                                                                                                                                          >> $dir/ctc_sai_meta_db.c
        echo ""                                                                                                                                                                                            >> $dir/ctc_sai_meta_db.c

        echo "sai_status_t ctc_sai_metadata_generic_get_sai_object_type_"$obj"(const ctc_sai_object_meta_key_t *meta_key, uint32_t attr_count, sai_attribute_t *attr_list)"                                    >> $dir/ctc_sai_meta_db.c
        echo "{"                                                                                                                                                                                           >> $dir/ctc_sai_meta_db.c
        if [ "$is_obj" -eq 1 ]
        then
            if [ "$obj" == "fdb_flush" ] ||  [ "$obj" == "hostif_packet" ]
            then
                echo "    return SAI_STATUS_NOT_IMPLEMENTED;"                                                                                                                                              >> $dir/ctc_sai_meta_db.c
            else
                echo "    return sai_metadata_sai_"$api"_api->get_"$obj"_attribute(meta_key->objectkey.key.object_id, attr_count, attr_list);"                                                             >> $dir/ctc_sai_meta_db.c
            fi
        else
            echo "    return sai_metadata_sai_"$api"_api->get_"$obj"_attribute(&meta_key->objectkey.key."$obj", attr_count, attr_list);"                                                                   >> $dir/ctc_sai_meta_db.c
        fi
        echo "};"                                                                                                                                                                                          >> $dir/ctc_sai_meta_db.c
        echo ""                                                                                                                                                                                            >> $dir/ctc_sai_meta_db.c  
    fi
done < $temp/obj2api.temp

echo "char* ctc_sai_metadata_get_enum_value_name(ctc_sai_enum_metadata_t* metadata, int value)"                           >> $dir/ctc_sai_meta_db.c
echo "{"                                                                                                                  >> $dir/ctc_sai_meta_db.c
echo "    if (metadata == NULL)"                                                                                          >> $dir/ctc_sai_meta_db.c
echo "    {"                                                                                                              >> $dir/ctc_sai_meta_db.c
echo "        return NULL;"                                                                                               >> $dir/ctc_sai_meta_db.c
echo "    }"                                                                                                              >> $dir/ctc_sai_meta_db.c
echo ""                                                                                                                   >> $dir/ctc_sai_meta_db.c
echo "    uint32 i = 0;"                                                                                                  >> $dir/ctc_sai_meta_db.c
echo ""                                                                                                                   >> $dir/ctc_sai_meta_db.c
echo "    for (; i < metadata->valuescount; ++i)"                                                                         >> $dir/ctc_sai_meta_db.c
echo "    {"                                                                                                              >> $dir/ctc_sai_meta_db.c
echo "        if (metadata->values[i] == value)"                                                                          >> $dir/ctc_sai_meta_db.c
echo "        {"                                                                                                          >> $dir/ctc_sai_meta_db.c
echo "            return metadata->valuesnames[i];"                                                                       >> $dir/ctc_sai_meta_db.c
echo "        }"                                                                                                          >> $dir/ctc_sai_meta_db.c
echo "    }"                                                                                                              >> $dir/ctc_sai_meta_db.c
echo ""                                                                                                                   >> $dir/ctc_sai_meta_db.c
echo "    return NULL;"                                                                                                   >> $dir/ctc_sai_meta_db.c
echo "}"                                                                                                                  >> $dir/ctc_sai_meta_db.c
echo ""                                                                                                                   >> $dir/ctc_sai_meta_db.c

echo ""                                                                                                                   >> $dir/ctc_sai_meta_db.c  
echo "int ctc_sai_metadata_apis_query(sai_api_query_fn api_query, sai_apis_t *apis)"                                      >> $dir/ctc_sai_meta_db.c  
echo "{"                                                                                                                  >> $dir/ctc_sai_meta_db.c  
echo "    sai_status_t status = SAI_STATUS_SUCCESS;"                                                                      >> $dir/ctc_sai_meta_db.c  
echo "    int count = 0;"                                                                                                 >> $dir/ctc_sai_meta_db.c                      
echo "    if (api_query == NULL)"                                                                                         >> $dir/ctc_sai_meta_db.c  
echo "    {"                                                                                                              >> $dir/ctc_sai_meta_db.c  

cnt=${#api_list[@]}
for (( i = 0 ; i < cnt ; i++ ))                                                                                           
do                                                                                                                        
    echo "        sai_metadata_sai_"${api_list[$i]}"_api = NULL;"                                                         >> $dir/ctc_sai_meta_db.c  
    echo "        apis->"${api_list[$i]}"_api = NULL;"                                                                    >> $dir/ctc_sai_meta_db.c  
done                                                                                                                      
                                                                                                                          
echo "        return count;"                                                                                              >> $dir/ctc_sai_meta_db.c  
echo "    }"                                                                                                              >> $dir/ctc_sai_meta_db.c  
echo ""                                                                                                                   >> $dir/ctc_sai_meta_db.c  

for (( i = 0 ; i < cnt ; i++ ))                                                                                           
do                                                                                                                        
    API=$(echo ${api_list[$i]} | tr 'a-z' 'A-Z')                                                                          
    echo "    status = api_query(SAI_API_"$API", (void**)&sai_metadata_sai_"${api_list[$i]}"_api);"                       >> $dir/ctc_sai_meta_db.c
    echo "    apis->"${api_list[$i]}"_api = sai_metadata_sai_"${api_list[$i]}"_api;"                                      >> $dir/ctc_sai_meta_db.c
    echo "    if (status != SAI_STATUS_SUCCESS)"                                                                          >> $dir/ctc_sai_meta_db.c
    echo "    {"                                                                                                          >> $dir/ctc_sai_meta_db.c
    echo "        count++;"                                                                                               >> $dir/ctc_sai_meta_db.c
    echo "        char *name = ctc_sai_metadata_get_enum_value_name(&ctc_sai_metadata_enum_sai_status_t, status);"        >> $dir/ctc_sai_meta_db.c
    echo "        CTC_SAI_LOG_ERROR(SAI_API_UNSPECIFIED, \"failed to query api SAI_API_"$API": %s (%d)\", name, status);" >> $dir/ctc_sai_meta_db.c
    echo "    }"                                                                                                          >> $dir/ctc_sai_meta_db.c
    echo ""                                                                                                               >> $dir/ctc_sai_meta_db.c  
done                                                                                                                      

echo "    return count; /* number of unsuccesfull apis */"                                                                >> $dir/ctc_sai_meta_db.c
echo "}"                                                                                                                  >> $dir/ctc_sai_meta_db.c
rm $temp/obj2api.temp

#for sai_moduel_f in $(find $path/inc -type f -name '*.h' -type f ! -name 'sai.h' -type f ! -name 'saistatus.h' -type f ! -name 'saitypes.h' | sort )

for sai_moduel_f in $(find $path/inc -type f -name '*.h' -type f ! -name 'sai.h' -type f ! -name 'saistatus.h' | sort )
do
    awk -f $path/centec/cli/script/enum.awk $sai_moduel_f >> $dir/ctc_sai_meta_db.c
done

for sai_moduel_f in $(find $path/inc -type f -name '*.h' -type f ! -name 'sai.h' -type f ! -name 'saistatus.h' | sort )
do
    awk -f $path/centec/cli/script/attr.awk $sai_moduel_f >> $dir/ctc_sai_meta_db.c
done

awk -f $path/centec/cli/script/enum.awk   $path/meta/saimetadatatypes.h  >> $dir/ctc_sai_meta_db.c
awk -f $path/centec/cli/script/enum.awk   $path/meta/saimetadatalogger.h >> $dir/ctc_sai_meta_db.c
awk -f $path/centec/cli/script/object.awk $path/inc/saitypes.h           >> $dir/ctc_sai_meta_db.c
