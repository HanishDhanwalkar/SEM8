import numpy as np
import roboticstoolbox as rtb
from roboticstoolbox import DHRobot, RevoluteMDH

class IndustrialBot(DHRobot):
    def __init__(self):
        self.dof = 2
        # self.q = np.zeros(self.dof)
        
        # self.DHparams={
        #     'a':    [0.0,   305.0,      0.0,    250.0,      0.0,        0.0],
        #     'alpha':[0.0,   np.pi/2,    np.pi/2,    0.0,    np.pi/2,    0.0],
        #     'd':    [0.0,   740.0,      1075.0, 0.0,        1275.0,     240.0]
        # }
        
        self.DHparams={
            'a':    [0.0,   305.0,   ],
            'alpha':[0.0,   np.pi/2, ],
            'd':    [0.0,   740.0,   ]
        }
        
        L = []
        
        for i in range(self.dof):
            L.append(
                RevoluteMDH(
                    a=self.DHparams['a'][i],
                    alpha=self.DHparams['alpha'][i],
                    d=self.DHparams['d'][i],
            ))
        
        super().__init__(
            L
        )
        
        # self.qz = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

        # self.addconfiguration("qz", self.qz)
        
        
        
if __name__ == "__main__":
    # bot = rtb.models.DH.Panda()
    bot = IndustrialBot()
    # print(bot.qz)
    
    cir = [0.0, np.pi/4, 3*np.pi/4, np.pi, 5*np.pi/4, 3*np.pi/2 ,7*np.pi/4 ,2*np.pi ,]
    
    tethas = np.array([np.array([x, 0.0]) for x in cir])
    
    # bot.plot(bot.qz, backend='pyplot', block=True)
    bot.plot(q=tethas, backend='pyplot', block=True, dt=0.2)

    
    