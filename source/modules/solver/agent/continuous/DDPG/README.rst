******************************************
Gradient-Free Policy Target (GFPT)
******************************************

Extension of DQN to continuous action domains. 
The policy network :math:`\pi_\theta(s)` is trained to maximize the mean square error

.. math::

    L(\theta) = \mathbb{E}_s[(\pi_\theta(s)-\tilde a)^2]

where :math:`\tilde a` is found by optimizing the deep Q-network using CMA-ES.

