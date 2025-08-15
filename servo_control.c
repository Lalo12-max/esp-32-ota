#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/adc.h"
#include "driver/gpio.h"

#define LED_GPIO         GPIO_NUM_2
#define POT_ADC_CHANNEL  ADC1_CHANNEL_6 // GPIO34

void app_main(void) {
    // Configurar ADC para leer el potenciómetro
    adc1_config_width(ADC_WIDTH_BIT_10); // Rango 0-1023
    adc1_config_channel_atten(POT_ADC_CHANNEL, ADC_ATTEN_DB_11); // hasta ~3.3V

    // Configurar LED como salida
    gpio_reset_pin(LED_GPIO);
    gpio_set_direction(LED_GPIO, GPIO_MODE_OUTPUT);

    while (1) {
        // Leer valor del potenciómetro
        int raw = adc1_get_raw(POT_ADC_CHANNEL);

        // Encender LED si el valor del potenciómetro supera cierto umbral
        if (raw > 512) {
            gpio_set_level(LED_GPIO, 1);
        } else {
            gpio_set_level(LED_GPIO, 0);
        }

        printf("Potenciómetro: %d, LED: %s\n", 
               raw, raw > 512 ? "ON" : "OFF");

        vTaskDelay(pdMS_TO_TICKS(200));
    }
}


