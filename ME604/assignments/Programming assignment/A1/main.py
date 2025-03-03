import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
from spatialmath import SE3
from scipy.interpolate import interp1d

rig_ang = np.deg2rad(90)


class IndustrialBot(DHRobot):
    def __init__(self):
        self.dof = 6
        # self.q = np.zeros(self.dof)
        
        # self.DHparams={
        #     'a':    [0.0,   305.0,      0.0,    250.0,      0.0,        0.0],
        #     'alpha':[0.0,   0.0,    np.pi/2,    0.0,    np.pi/2,    0.0],
        #     'd':    [0.0,   740.0,      1075.0, 0.0,        1275.0,     240.0]
        # }
        
        self.DHparams={
            'a':    [305.0,      1075.0,    250.0,      0.0,        240.0,       0.0],
            'alpha':[-rig_ang,   0.0,       -rig_ang,   rig_ang,    rig_ang,       0.0],
            'd':    [740.0,      0.0,       0.0,        1275.0,     0.0,     0.0]
        }
        
        links = []
        
        for i in range(self.dof):
            links.append(
                RevoluteDH(
                    a=self.DHparams['a'][i],
                    alpha=self.DHparams['alpha'][i],
                    d=self.DHparams['d'][i],
            ))
        
        super(IndustrialBot, self).__init__(links, name="A1")
        
        self.qz = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        self.zero_configuration = np.array([0.0, -rig_ang, 0.0, 0.0, -rig_ang, 0.0])
        self.max_height_q = np.array([0.0, -rig_ang, -rig_ang, 0.0, -rig_ang, 0.0])
        
        self.addconfiguration("qz", self.qz)
        self.addconfiguration("zero_configuration", self.zero_configuration)
        self.addconfiguration("max_height_q", self.max_height_q)
        
        
        
if __name__ == "__main__":
    # bot = rtb.models.DH.Panda()
    bot = IndustrialBot()
    print(bot.qz)
    
    # cir = [0.0, np.pi/4, 3*np.pi/4, np.pi, 5*np.pi/4, 3*np.pi/2 ,7*np.pi/4 ,2*np.pi]
    space = np.linspace(0.0, 1.0, 20)
    cir = [x * 2*np.pi for x in space]
    
    tethas = np.array([np.array([x, -rig_ang+x, x, x, x, x]) for x in cir])
    # print(tethas)
        
        
    ## Q1
    # bot.plot(bot.qz, backend='pyplot', block=True)
    # plot = bot.plot(q=tethas, backend='pyplot', block=True, dt=0.5, eeframe=True, jointaxes=True)
    # plot = bot.plot(q=bot.zero_configuration, backend='pyplot', block=True, dt=0.5, eeframe=True, jointaxes=True)


    ## Q2
    # start_q = bot.zero_configuration
    # end_q = bot.max_height_q
    
    # num_of_intermidiate_steps = 5

    # linfit = interp1d([1,num_of_intermidiate_steps], np.vstack([start_q, end_q]), axis=0)
    # path = linfit([i for i in range(1, num_of_intermidiate_steps+1)])
    # print(path)
    # bot.plot(path, backend='pyplot', block=True, dt=0.5, movie='A1/mov.gif')
