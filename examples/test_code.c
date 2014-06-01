
float Gain_Gain = 5;

float Constant_Value = 12.3;

float Constant1_Value = 34.5;
float Const1_U = 10.4;

float out = 0;

/* Model step function */
void Const1_step(void)
{
  /* Gain: '<Root>/Gain' incorporates:
   *  Constant: '<Root>/Constant'
   */
  //Const1_Y.Out1 = Const1_P.Gain_Gain * Const1_P.Constant_Value;
    out = Gain_Gain * Constant_Value;

  /* Product: '<Root>/Product' incorporates:
   *  Constant: '<Root>/Constant1'
   */
  //Const1_Y.Out1 *= Const1_P.Constant1_Value;
  out *= Constant1_Value;

  /* Sum: '<Root>/Sum' incorporates:
   *  Inport: '<Root>/In1'
   */
  //Const1_Y.Out1 += Const1_U.In1;
  out  += Const1_U;

}


int main()
{
}
