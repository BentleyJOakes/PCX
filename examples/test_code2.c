
float Gain_Gain = 5;

float Constant_Value = 12.3;

float Constant1_Value = 34.5;
float Const1_U = 10.4;

float out = 0;


int main()
{
    out = Gain_Gain * Constant_Value;

  out *= Constant1_Value;
  out  += Const1_U;
}
