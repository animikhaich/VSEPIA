//THE PURPOSE OF THIS CODE IS TO IMPLEMENT POWER SAVING FEATURE WHICH REDUCES THE POWER CONSUMPTION FROM mAmps TO uAmps....

//-----------------------------------------------------------------------

//THE MAIN WORKING OF THIS CODE:-

//BY DEFAULT THE ARDUINO IS ON SLEEP MODE.
//WHEN A SERIAL INPUT IS READ,IT WAKES UP,GIVES THE DISTANCE READINGS FOR 10 TRIALS AND GOES BACK TO SLEEP AGAIN AND WAKES UP WHENEVER WE SEND A SERIAL INPUT.....   

//----------------------------------------------------------------------
//CODE STARTS HERE

#include <avr/sleep.h> //HEADER FILE TO BE INCLUDED FOR SLEEP MODE 

const int trig = 8;      //INITIALIZE PIN8 TO SEND THE TIGGER SIGNAL TO THE SENSOR FOR TRIGGERING THE SENSOR OPERATION   
const int echo = 9;      //INITIALIZE PIN9 TO READ THE OUPTUT FROM THE SENSOR 
const int vcc = 10;

float duration,distance;         //DECLARE VARIABLES DISTANCE AND DURATION
int count = 0;                   // COUNTER 
int wakePin = 2;                 // PIN USED TO WAKE UP THE ARDUINO 

void wakeupnow()
{
    //AN EMPTY FUNCTION WHICH JUST WAKES THE CONTROLLER FROM SLEEP  ........ 
}



void sleepnow()         
{
    attachInterrupt(0,wakeupnow, LOW); // WHENEVER THE INTERRUPT_0 (PIN2) SENSES LOW SIGNAL....CALL WAKEUPNOW FUNCTION 
   
    set_sleep_mode(SLEEP_MODE_PWR_DOWN);  
 
    sleep_enable();          // ENABLES THE SLEEP BIT IN THE MCU REGISTER 
    
    sleep_mode();            // CONTROLLER GOES TO SLEEP
    
    sleep_disable();         //DISABLE THE SLEEP AS SOONS AS THE CONTROLLER WAKES UP
    
    detachInterrupt(0);      //DETACH THE INTERRUPT ON PIN2 
 
}


void setup()
{
    pinMode(vcc,OUTPUT);
    pinMode(trig,OUTPUT);   //PIN 8(DECLARED AS TRIGGER PIN) IS SET TO OUTPUT MODE THROUGH WHICH WE SEND THE TRIGGER SIGNAL
    pinMode(echo,INPUT);    //PIN 9(DECLARED AS ECHO PIN) IS SET TO INPUT MODE THROUGH WHICH WE READ THE SENSOR OUTPUT
    Serial.begin(9600);     //BAUD RATE OF 9600 IS SET 
    pinMode(wakePin, INPUT);//PIN 2(DECLARED AS WAKEPIN) IS SET TO INPUT MODE
    digitalWrite(vcc, LOW);
}

void loop()
{
    while(Serial.available())            //SENSES THE AVAILABILITY OF INPUT IN THE SERIAL PORT 
    {
        int val = Serial.read();         //READ THE INPUT FROM THE SERIAL PORT  
        while( val=='S' && count<=10)    //UNTIL THE CHARACTER 'S' IS SENT AND THE COUNT IS WITHIN 10-----PERFORM THE FOLLOWING 
        {
            digitalWrite(vcc, HIGH);
            
            if (count == 0)
              delay(1000);
              
            digitalWrite(trig,LOW);
            delayMicroseconds(2);
            //GENERATE A LOW SIGNAL ON TRIG PIN FOR 2 MICROSECONDS 
            
            digitalWrite(trig,HIGH);
            delayMicroseconds(10);
            //GENERATE A HIGH SIGNAL ON TRIG PIN FOR 10 MICROSECONDS 
            
            digitalWrite(trig,LOW);
            //GENERATE LOW SIGNAL AGAIN ON TRIG PIN FOREVER 
            
            duration=pulseIn(echo,HIGH);  //IT RETURNS THE TIME PERIOD UPTO WHICH ECHO PIN INPUT IS HIGH(WHICH INCLUDES BOTH TO AND FRO MOTION) 
            distance=duration*0.034/2;    //FINDING THE DISTANCE FROM TIME MEASURED 
            Serial.println(distance);     //PRINT THE DISTANCE
            count++;                      //INCREMENT COUNT FOR 10 TRIALS WHICH GIVES US 10 DISTANCE VALUES
            delay(250);                   //10 DISTANCE VALUES MEASURED WITH 250 ms DELAY BETWEEN EACH TRIAL   
        }
        count=0;                          //COUNT RESET TO '0'
        digitalWrite(vcc, LOW);
        sleepnow();                       //CALL THE SLEEPNOW FUNCTION WHICH PUTS THE CONTROLLER TO SLEEP MODE 
    
    }

}
