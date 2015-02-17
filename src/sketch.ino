
int volt_div_pin  = A0;
int relay_pin     = 12;
int aux_pin       = 11;
int aux_pin_state = 0;
int now           = 0;
int voltage_warn  = 0;
int last_voltage  = -1;
int wait_time     = 120;

unsigned long  start_time = 0;

// Based on http://www.energymatters.com.au/components/battery-voltage-discharge/ 
float shut_off_voltage   = 12.20;
float power_on_voltage   = 12.70;
float voltage     = 0;


void wait(int seconds)
{
    for (int i = 0; i <= seconds; i++)
    {
        delay(1000);
    }
}


void relay_on(int pin)
{
    if (pin == aux_pin)
    {
        aux_pin_state = 1;
    }

    digitalWrite(pin, LOW);
    delay(1000);
}


void relay_off(int pin)
{
    if (pin == aux_pin)
    {
        aux_pin_state = 0;
    }

    digitalWrite(pin, HIGH);
    delay(1000);
}


void low_voltage_routine()
{
    relay_off(aux_pin);
} 


void nominal_voltage_routine()
{
    relay_on(aux_pin);
}


void setup()
{
    Serial.begin(9600);

    pinMode(volt_div_pin, INPUT);

    relay_on(relay_pin);
    relay_off(relay_pin);
    relay_off(aux_pin);
    
    pinMode(relay_pin,    OUTPUT);
    pinMode(aux_pin,      OUTPUT);

    Serial.println("ready");
    Serial.flush();

}


void loop()
{

    float avg_voltage = 0;
    float raw_input   = 0;
    
    relay_on(relay_pin);
    
    raw_input = analogRead(volt_div_pin);
    voltage = ((raw_input/1024) * 5)/.32;

    /* Basically this triple checks that the voltage is low so we don't sit there  
       and flip the relay on and off just because it had an incorrect reading */  
    if (voltage <= shut_off_voltage)
    {
            if (voltage_warn < 3)
            {
                voltage_warn++;
            }   
    }

    else
    {

        if (voltage_warn > 0)
        {
            voltage_warn--;
        }

    }
    
    if (voltage_warn == 3)
    {
        low_voltage_routine();
    }

    
    else if (voltage >= power_on_voltage && aux_pin_state == 0)
    {
        nominal_voltage_routine();
    }
    
    /* Turn voltage into an int */
    last_voltage = voltage * 100;

    
    relay_off(relay_pin);

    /* Output the voltage in an easy format */
    Serial.print(last_voltage);
    Serial.print(":");
    Serial.print(voltage_warn);
    Serial.print(":");
    Serial.println(aux_pin_state);
    Serial.flush();


    wait(wait_time); 
}
