from RS_neurone_class import RS_neurone
import vrep
import math
import time



# Paramètres des neurones de Rowat Selweston -----------------------------------------------------

Amplitude = 0.3 # contrôle la stabilité du robot.
tau_s = 3.5     # ---
tau_m = 0.30    # contrôle l'amplitude du signal.
sigma_f = 0.5   # ---
sigma_s = 1     # ---
dt = 0.1        # contrôle la vitesse d'oscillation.
tau_max = 80    # contrôle la vitesse d'oscillation.

# Conditions initiales ----------------------------------------------------------------------------

phase = math.pi/3
pulsation = 10*math.pi/9
V_initial = 0
q_initial = 0

# Définition des fonctions ------------------------------------------------------------------------

def to_rad(deg):
    return 2*math.pi*deg/360

def to_deg(rad):
    return rad*360/(2*math.pi)


def RS_neurone_control(Amplitude,tau_s,tau_m,sigma_f,sigma_s,dt,tau_max,V_initial,q_initial,pulsation,phase) :
    # Le neurone de Rowat Selveston
    RSNeurone = RS_neurone(Amplitude,tau_s,tau_m,sigma_f,sigma_s,dt,tau_max)
    # Definition des oscillateurs
    Oscillateur = RSNeurone.compute_solution_sinusoidal(V_initial,q_initial,pulsation,phase)
    return Oscillateur[1]

def Sinusoidal_function(t,pulsation,phase) :
    return math.sin( pulsation*t + phase )

# simulation config --------------------------------------------------------------------------------

ip = '127.0.0.1'
port = 19997
scene = './snake.ttt'
position_init = [0,0,0]

# La simulation -------------------------------------------------------------------------------------


print ('Simulation started')
vrep.simxFinish(-1)                                 # just in case, close all opened connections
client_id=vrep.simxStart(ip,port,True,True,5000,5)  # Connect to V-REP


if client_id!=-1:
    
    print ('Connected to remote API server on %s:%s' % (ip, port))
    res = vrep.simxLoadScene(client_id, scene, 1, vrep.simx_opmode_blocking)
    res, snake = vrep.simxGetObjectHandle(client_id, 'snake', vrep.simx_opmode_blocking)
    res, h1_motor = vrep.simxGetObjectHandle(client_id, 'snake_joint_h1', vrep.simx_opmode_blocking)
    res, h2_motor = vrep.simxGetObjectHandle(client_id, 'snake_joint_h2', vrep.simx_opmode_blocking)
    res, h3_motor = vrep.simxGetObjectHandle(client_id, 'snake_joint_h3', vrep.simx_opmode_blocking)
    res, h4_motor = vrep.simxGetObjectHandle(client_id, 'snake_joint_h4', vrep.simx_opmode_blocking)
    res, v1_motor = vrep.simxGetObjectHandle(client_id, 'snake_joint_v1', vrep.simx_opmode_blocking)
    res, v2_motor = vrep.simxGetObjectHandle(client_id, 'snake_joint_v2', vrep.simx_opmode_blocking)
    res, v3_motor = vrep.simxGetObjectHandle(client_id, 'snake_joint_v3', vrep.simx_opmode_blocking)
    res, v4_motor = vrep.simxGetObjectHandle(client_id, 'snake_joint_v4', vrep.simx_opmode_blocking)
     
    vrep.simxStartSimulation(client_id, vrep.simx_opmode_blocking)


    RS_neurone_compteur  = 2
    Sinusoidal_solution_compteur = 0
    
    choice = input('Do you want to control the snake with (0 = RS neurone) or (1 = sinusoidal function) ? (0/1) --> ')
            
    if choice == str(0) : 
        
        while(True) : 
        
            Oscillateur1 = RS_neurone_control(Amplitude,tau_s,tau_m,sigma_f,sigma_s,dt,tau_max,V_initial,q_initial,pulsation,2*phase)
            Oscillateur2 = RS_neurone_control(Amplitude,tau_s,tau_m,sigma_f,sigma_s,dt,tau_max,V_initial,q_initial,pulsation,4*phase)
            Oscillateur3 = RS_neurone_control(Amplitude,tau_s,tau_m,sigma_f,sigma_s,dt,tau_max,V_initial,q_initial,pulsation,6*phase)
            Oscillateur4 = RS_neurone_control(Amplitude,tau_s,tau_m,sigma_f,sigma_s,dt,tau_max,V_initial,q_initial,pulsation,8*phase)

            vrep.simxSetJointTargetPosition(client_id, v1_motor, Oscillateur1[RS_neurone_compteur], vrep.simx_opmode_blocking)
            vrep.simxSetJointTargetPosition(client_id, v2_motor, Oscillateur2[RS_neurone_compteur], vrep.simx_opmode_blocking)
            vrep.simxSetJointTargetPosition(client_id, v3_motor, Oscillateur3[RS_neurone_compteur], vrep.simx_opmode_blocking)
            vrep.simxSetJointTargetPosition(client_id, v4_motor, Oscillateur4[RS_neurone_compteur], vrep.simx_opmode_blocking)
            
            RS_neurone_compteur = RS_neurone_compteur + 1
            if RS_neurone_compteur == (len(Oscillateur1)) :
                RS_neurone_compteur = 2
    
    elif choice == str(1) :
        
        while(True) :
            
            vrep.simxSetJointTargetPosition(client_id, v1_motor, Sinusoidal_function(Sinusoidal_solution_compteur,math.pi/6,2*phase), vrep.simx_opmode_blocking)
            vrep.simxSetJointTargetPosition(client_id, v2_motor, Sinusoidal_function(Sinusoidal_solution_compteur,math.pi/6,4*phase), vrep.simx_opmode_blocking)
            vrep.simxSetJointTargetPosition(client_id, v3_motor, Sinusoidal_function(Sinusoidal_solution_compteur,math.pi/6,6*phase), vrep.simx_opmode_blocking)
            vrep.simxSetJointTargetPosition(client_id, v4_motor, Sinusoidal_function(Sinusoidal_solution_compteur,math.pi/6,8*phase), vrep.simx_opmode_blocking)
            
            Sinusoidal_solution_compteur = Sinusoidal_solution_compteur + 1
            
    vrep.simxFinish(client_id)

else:
    print('Unable to connect to %s:%s' % (ip, port))
    
# -----------------------------------------------------------------------------------------------------------------------------------
