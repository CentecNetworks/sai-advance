
#build sai dynamic lib
INCLUDE_DIRECTORIES(${SAIPROJECT_SOURCE_DIR}/inc)

INCLUDE_DIRECTORIES(${SDKHOME}/core)
INCLUDE_DIRECTORIES(${SDKHOME}/sal/include)
INCLUDE_DIRECTORIES(${SDKHOME}/dal/include)
INCLUDE_DIRECTORIES(${SDKHOME}/core/init)
INCLUDE_DIRECTORIES(${SDKHOME}/core/app)
INCLUDE_DIRECTORIES(${SDKHOME}/core/common/include)
INCLUDE_DIRECTORIES(${SDKHOME}/dkits)
INCLUDE_DIRECTORIES(${SDKHOME}/core/api/include)

INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/inc)
AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR}/src SRC_LIST)

IF(${CONFIG_PLATFORM} STREQUAL "ctc")
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/platform)
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/platform/inc)
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/platform/driver/macled_handle)
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/platform/driver/i2c_handle)
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/platform/driver/fiber_handle)

AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR}/platform/mgt PLAT_SRC_LIST1)
AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR}/platform/driver/macled_handle PLAT_SRC_LIST2)
AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR}/platform/driver/i2c_handle PLAT_SRC_LIST3)
AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR}/platform/driver/fiber_handle PLAT_SRC_LIST4)
ENDIF(${CONFIG_PLATFORM} STREQUAL "ctc")

IF(CONFIG_SAICLI)
ADD_DEFINITIONS(-DCTC_SAI_CLI)

INCLUDE_DIRECTORIES(${SDKHOME}/libctccli/include)
INCLUDE_DIRECTORIES(${SDKHOME}/ctccli/sdkcli)
INCLUDE_DIRECTORIES(${CMAKE_CURRENT_SOURCE_DIR}/cli/inc)

AUX_SOURCE_DIRECTORY(${CMAKE_CURRENT_SOURCE_DIR}/cli/src CLI_SRC_LIST)
ENDIF(CONFIG_SAICLI)

LINK_DIRECTORIES(${SAIPROJECT_SOURCE_DIR}/lib/${CHIPNAME})
ADD_LIBRARY(sai SHARED ${SRC_LIST} ${PLAT_SRC_LIST1} ${PLAT_SRC_LIST2} ${PLAT_SRC_LIST3} ${PLAT_SRC_LIST4} ${CLI_SRC_LIST})
TARGET_LINK_LIBRARIES(sai ctcsdk)

IF(CONFIG_DBCLIENT)
    INCLUDE_DIRECTORIES(${REDIS_INCLUDE_DIR})
    TARGET_LINK_LIBRARIES(sai geohash)
    TARGET_LINK_LIBRARIES(sai hiredis)
ENDIF(CONFIG_DBCLIENT)

SET_TARGET_PROPERTIES(sai PROPERTIES VERSION 1 SOVERSION 1.5)

SET(LIBRARY_OUTPUT_PATH ${SAIPROJECT_SOURCE_DIR}/lib/${CHIPNAME})

MESSAGE(STATUS "This is OUT LIB dir "${LIBRARY_OUTPUT_PATH})
