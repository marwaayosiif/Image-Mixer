## This is the abstract class that the students should implement  

from modesEnum import Modes
import numpy as np
import cv2

class ImageModel():

    """
    A class that represents the ImageModel"
    """

    # def __init__(self):
    #     pass

    def __init__(self, imgPath: str):
        self.imgPath = imgPath
        ###
        # ALL the following properties should be assigned correctly after reading imgPath 
        ###
        self.imgByte = cv2.imread(self.imgPath,0)
        f = np.fft.fft2(self.imgByte)
        self.dft = np.fft.fftshift(f)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft) 
        magnitudelog = 20*np.log((self.magnitude))
        self.magnitudeInverse = np.asarray(magnitudelog,dtype=np.uint8)
        self.phase = np.angle(self.dft)
        self.phaseInverse = np.asarray(self.phase,dtype=np.uint8)
   
    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        """
        a function that takes ImageModel object mag ratio, phase ration 
        """
        if mode == Modes.magnitudeAndPhase:
            firstcomp1 =self.magnitude*(magnitudeOrRealRatio/100)
            secondcomp1 =imageToBeMixed.magnitude*(1-(magnitudeOrRealRatio/100))
            comp1 = firstcomp1 + secondcomp1
            firstcomp2 =imageToBeMixed.phase*(phaesOrImaginaryRatio/100)
            secondcomp2 =self.phase*(1-(phaesOrImaginaryRatio/100))
            comp2 = firstcomp2 + secondcomp2
            picture = np.multiply(comp1, np.exp(1j*comp2))
            invfsh = np.fft.ifftshift(picture)
            invf = np.fft.ifft2(invfsh)
            real = np.real(invf)
            return real
        elif mode == Modes.realAndImaginary :  
            firstcomp1 =self.real*(magnitudeOrRealRatio/100)
            secondcomp1 =imageToBeMixed.real*(1-(magnitudeOrRealRatio/100))
            comp1 = firstcomp1 + secondcomp1
            firstcomp2 =imageToBeMixed.imaginary*(phaesOrImaginaryRatio/100)
            secondcomp2 =self.imaginary*(1-(phaesOrImaginaryRatio/100))
            comp2 = firstcomp2 + secondcomp2
            picture = comp1 + 1j*comp2
            invfsh = np.fft.ifftshift(picture)
            invf = np.fft.ifft2(invfsh)
            real = np.real(invf)
            return real
    def mixUniform(self, imageToBeMixed: 'ImageModel', SliderValue:float, mode: 'Modes') -> np.ndarray:
        if mode == Modes.uniformMagitudeAndPhase:
            comp1 =np.divide(self.magnitude,self.magnitude) 
            firstcomp2 = imageToBeMixed.phase*(SliderValue/100)
            secondcomp2 = self.phase*(1-(SliderValue/100))
            comp2 = firstcomp2+secondcomp2
            picture = np.multiply(comp1, np.exp(1j*comp2))
            invfsh = np.fft.ifftshift(picture)
            invf = np.fft.ifft2(invfsh)
            real = np.real(invf)
            real *= 225.0/np.max(real)
            return real
        elif mode == Modes.uniformMagitudeAnduniformPhase:
            comp1 =np.divide(self.magnitude,self.magnitude)
            comp2 =imageToBeMixed.phase*0
            picture = np.multiply(comp1, np.exp(1j*comp2))
            invfsh = np.fft.ifftshift(picture)
            invf = np.fft.ifft2(invfsh)
            real = np.real(invf)
            real *= 225.0/np.max(real)
            return real
        elif mode == Modes.uniformPhaseAndMagnitude:
            comp1=self.phase*0
            firstcomp2= imageToBeMixed.magnitude*(SliderValue/100)
            secondcomp2 = self.magnitude*(1-(SliderValue/100))
            comp2=firstcomp2+secondcomp2
            picture = np.multiply(comp2,np.exp(1j*comp1))  
            invfsh = np.fft.ifftshift(picture)
            invf = np.fft.ifft2(invfsh)
            real = np.real(invf)
            real *= 225.0/np.max(real)
            return real  
        elif mode == Modes.uniformPhaseAnduniformMagnitude :  
            comp1=self.phase*0
            comp2=np.divide(imageToBeMixed.magnitude,imageToBeMixed.magnitude)
            picture = np.multiply(comp2,np.exp(1j*comp1))  
            invfsh = np.fft.ifftshift(picture)
            invf = np.fft.ifft2(invfsh)
            real = np.real(invf)
            real *= 225.0/np.max(real)
            return real 



