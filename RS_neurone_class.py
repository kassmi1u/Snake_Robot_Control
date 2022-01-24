import math
from multiprocessing import AuthenticationError 
import numpy as np 
from matplotlib import pyplot as plt


# Omar KASSMI

class RS_neurone() : 
    
    # Constructeur
    def __init__(self,A_f,tau_s,tau_m,sigma_f,sigma_s,dt,tau_max) :
        self.Af = A_f
        self.taus = tau_s
        self.taum = tau_m
        self.sigmaf = sigma_f
        self.sigmas = sigma_s
        self.dt = dt
        self.taumax = tau_max
        self.n_steps = int(self.taumax/self.dt)
        
        
    # distribution de dirac 
    def dirac_distribution(self,iterations) :
        step = iterations*self.dt
        if step >= 1 and step <=2 :
            return 1
        return 0
    
    
    # distribution sinusoidale
    def sinusoidal_distribution(self,nbre_steps,pulsation,phase) : 
        t = nbre_steps*self.dt
        return math.sin(pulsation*t+phase)
        
    
        
    def F(self,V) : 
        return V - self.Af*math.tanh(self.sigmaf*V/self.Af)
    
    
    # La derivee de V
    def derivative_of_q(self,V,q) :
        
        return ( -q +self.sigmas*V)/self.taus
       
       
    # La derivee de q 
    def derivative_of_V(self,V,Iinj,q) :
        return -(self.F(V)+q-Iinj)/self.taum
    
    
    # solution de l'equation differentielle selon la méthode d'euler
    def solution_differential_equation (self,V,q,Iinj) :
        
        q = q + self.dt*self.derivative_of_q(V,q)
        V = V + self.dt*self.derivative_of_V(V,Iinj,q)
        return q,V
    
    
    # Calcul de la solution avec une distribution de dirac 
    def compute_solution_dirac(self,V,q) : 
        V_value = V
        q_value = q 
        V_solutions = [V]
        q_solutions = [q]
        interne_signal_values = [0]
        for i in range(self.n_steps) :
            interne_signal = self.dirac_distribution(i) 
            q_value,V_value = self.solution_differential_equation(V_value,q_value,interne_signal)
            V_solutions.append(V_value)
            q_solutions.append(q_value)
            interne_signal_values.append(interne_signal)
        return interne_signal_values, V_solutions, q_solutions
    
    
    # Calcul de la solution avec une distribution sinusoidal
    def compute_solution_sinusoidal(self,V,q,pulsation,phase) :
        V_value = V
        q_value = q 
        V_solutions = [V]
        q_solutions = [q]
        interne_signal_values = [0]
        for i in range(self.n_steps) :
            interne_signal = self.sinusoidal_distribution(i,pulsation,phase) 
            q_value,V_value = self.solution_differential_equation(V_value,q_value,interne_signal)
            V_solutions.append(V_value)
            q_solutions.append(q_value)
            interne_signal_values.append(interne_signal)
        return interne_signal_values, V_solutions, q_solutions
    
    
    def compute_solution_couplage_deux_neurones(self,V,q,poid1,poid2,epsilon) :
        V_value1 = V + epsilon
        V_value2 = V - epsilon
        q_value1 = q
        q_value2 = q 
        V_solutions1 = [V_value1]
        V_solutions2 = [V_value2]
        q_solutions1 = [q_value1]
        q_solutions2 = [q_value2]
        for i in range(self.n_steps) :
            q_value1,V_value1 = self.solution_differential_equation(V_value1,q_value1,poid2*V_value2)
            V_solutions1.append(V_value1)
            q_solutions1.append(q_value1)
            q_value2,V_value2 = self.solution_differential_equation(V_value2,q_value2,poid1*V_value1)
            V_solutions2.append(V_value2)
            q_solutions2.append(q_value2)
        return V_solutions1,V_solutions2
        
    
    
    # Affichage des graphes
    def plot_solution(self,interne_signal,V_solution,title) : 
        plt.plot(interne_signal)
        plt.plot(V_solution)
        plt.title(title)
        plt.show()
        
        
    
    
    


            
        
            
            
            
    