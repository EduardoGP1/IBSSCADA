// Pino onde o Termistor esta conectado
#define PINOTERMISTOR A0         
// Valor do termistor na temperatura nominal
#define TERMISTORNOMINAL 20000      
// Temp. nominal descrita no Manual
#define TEMPERATURENOMINAL 25   
// Número de amostragens para 
#define NUMAMOSTRAS 5
// Beta do nosso Termistor
#define BCOEFFICIENT 3977
// valor do resistor em série
#define SERIESRESISTOR 9800    
 
int amostra[NUMAMOSTRAS];
int i;
void setup(void) {
  Serial.begin(9600);
  analogReference(EXTERNAL);
}
 
void loop(void) {
  float media;
 
  for (i=0; i< NUMAMOSTRAS; i++) {
   amostra[i] = analogRead(PINOTERMISTOR);
   delay(10);
  }
 
  media = 0;
  for (i=0; i< NUMAMOSTRAS; i++) {
     media += amostra[i];
  }
  media /= NUMAMOSTRAS;

  // Converte o valor da tensão em resistência
  media = 1023 / media - 1;
  media = SERIESRESISTOR / media;
  
  //Faz o cálculo pela fórmula do Fator Beta
  float temperatura;
  temperatura = media / TERMISTORNOMINAL;     // (R/Ro)
  temperatura = log(temperatura); // ln(R/Ro)
  temperatura /= BCOEFFICIENT;                   // 1/B * ln(R/Ro)
  temperatura += 1.0 / (TEMPERATURENOMINAL + 273.15); // + (1/To)
  temperatura = 1.0 / temperatura;                 // Inverte o valor
  temperatura -= 273.15;                         // Converte para Celsius
 
  Serial.print("Temperatura no Sensor eh: ");
  Serial.print(temperatura);
  Serial.println(" *C");
 
  delay(1000);
}
