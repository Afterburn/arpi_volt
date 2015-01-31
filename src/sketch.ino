
int volt_div_pin  = A0;
int relay_pin     = 12;
int aux_pin       = 11;
int aux_pin_state = 0;
unsigned long  start_time = 0;
int now           = 0;
int voltage_warn  = 0;
float low_voltage   = 12.00;
float voltage     = 0;
float raw_input   = 0;
int last_voltage  = -1;

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


void reset_timer()
{
    start_time = 0;
}

void start_timer()
{
    start_time = millis();
}

unsigned long elapsed_time()
{
    return millis() - start_time;
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
    
    relay_on(relay_pin);
    
    raw_input = analogRead(volt_div_pin);
    voltage = ((raw_input/1024) * 5)/.32;

    if (voltage < low_voltage)
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
        reset_timer();
    }

    else if (voltage_warn == 0)
    {
        if (aux_pin_state == 0 && start_time == 0)
        {
            start_timer();
        }
        
        else if (aux_pin_state == 0 && start_time != 0 && elapsed_time() >= 300000)
        {
            nominal_voltage_routine();
            reset_timer();
        }
    }

    last_voltage = voltage * 100;

    relay_off(relay_pin);

    Serial.print(last_voltage);
    Serial.print(":");
    Serial.print(voltage_warn);
    Serial.print(":");
    Serial.println(aux_pin_state);
    //Serial.print(":");
    //Serial.println(elapsed_time());
    Serial.flush();


    wait(30); 
}
