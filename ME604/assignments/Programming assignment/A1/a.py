import roboticstoolbox as rtb
import numpy as np


panda = rtb.models.DH.Panda()

panda.q = panda.qr

q = np.random.rand(100, 7)

# Plot the joint trajectory with a 50ms delay between configurations
panda.plot(q=q, backend='pyplot', dt=0.050, vellipse=True, fellipse=True)