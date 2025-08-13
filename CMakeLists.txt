# The following four lines of boilerplate have to be in your project's CMakeLists
# in this exact order for cmake to work correctly
cmake_minimum_required(VERSION 3.16)


include($ENV{IDF_PATH}/tools/cmake/project.cmake)

# Configurar tabla de particiones personalizada
set(PARTITION_TABLE_CSV_PATH "${CMAKE_CURRENT_SOURCE_DIR}/partitions.csv")

project(mqtt_ssl)

target_add_binary_data(mqtt_ssl.elf "main/emqxsl_ca.pem" TEXT)
