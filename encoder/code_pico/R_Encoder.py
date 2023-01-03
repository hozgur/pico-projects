import machine
import time

class R_Encoder:
    
    def __init__(self, A_Pin, B_Pin, Z_Pin):
        self.A_Pin = A_Pin
        self.B_Pin = B_Pin
        self.Z_Pin = Z_Pin
        self.Enc_Counter = 0
        self.Enc_A_State = 0
        self.Enc_B_State = 0
        self.Enc_Z_State = 0
        self.rev_Counter = 0
        self.error = 0        
        
        self.Setup_Irqs()
        
    def Reset_Counter(self):
        self.Enc_Counter = 0
        self.rev_Counter = 0
        
    def show(self):
        print("Rotary Encoder: ", self.Enc_Counter)
        print("Revolution: ", self.rev_Counter)
    
    def Enc_Handler_A(self, Pin):
        self.Enc_A_State = self.Enc_Pin_A.value()
        self.Enc_B_State = self.Enc_Pin_B.value()
        self.Enc_Z_State = self.Enc_Pin_Z.value()
        
        if self.Enc_A_State == 0:
            if self.Enc_B_State == 1:
                self.Enc_Counter += 1
                #print("AFALL Saat Yönü A: ",self.Enc_A_State," B: ",self.Enc_B_State)
            elif self.Enc_B_State == 0:
                self.Enc_Counter -= 1
                #print("AFALL Saat Ters A: ",self.Enc_A_State," B: ",self.Enc_B_State)
            else:
                print("A Falling Error")
                
        elif self.Enc_A_State == 1:
            
            if self.Enc_Z_State == 1:
                self.rev_Counter += 1
                
            if self.Enc_B_State == 0:
                self.Enc_Counter += 1
                #print("ARISE Saat Yönü A: ",self.Enc_A_State," B: ",self.Enc_B_State)
                #print(self.Enc_Counter)
            elif self.Enc_B_State == 1:
                self.Enc_Counter -= 1
                #print("ARISE Saat Ters A: ",self.Enc_A_State," B: ",self.Enc_B_State)
                #print(self.Enc_Counter)
            else:
                print("A Rising Error")
        else:
            print("Handler_A Error")
                
    def Enc_Handler_B(self, Pin):
        self.Enc_A_State = self.Enc_Pin_A.value()
        self.Enc_B_State = self.Enc_Pin_B.value()
        
        if self.Enc_B_State == 0:
            if self.Enc_A_State == 0:
                self.Enc_Counter += 1
                #print("BFALL Saat Yönü A: ",self.Enc_A_State," B: ",self.Enc_B_State)
                #print(self.Enc_Counter)
            elif self.Enc_A_State == 1:
                self.Enc_Counter -= 1
                #print("BFALL Saat Ters A: ",self.Enc_A_State," B: ",self.Enc_B_State)
                #print(self.Enc_Counter)
            else:
                print("B Falling Error")
                      
        elif self.Enc_B_State == 1:
            if self.Enc_A_State == 1:
                self.Enc_Counter += 1
                #print("BRISE Saat Yönü A: ",self.Enc_A_State," B: ",self.Enc_B_State)
                #print(self.Enc_Counter)
            elif self.Enc_A_State == 0:
                self.Enc_Counter -= 1
                #print("BRISE Saat Ters A: ",self.Enc_A_State," B: ",self.Enc_B_State)
                #print(self.Enc_Counter)
            else:
                print("B Rising Error")
        else:
            print("Handler_B Error")
        
            
    def Setup_Irqs(self):
        self.Enc_Pin_A = machine.Pin(self.A_Pin, machine.Pin.IN)
        self.Enc_Pin_A.irq(trigger=machine.Pin.IRQ_RISING, handler=self.Enc_Handler_A)
        self.Enc_Pin_B = machine.Pin(self.B_Pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        #self.Enc_Pin_B.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.Enc_Handler_B)
        self.Enc_Pin_Z = machine.Pin(self.Z_Pin, machine.Pin.IN)
        