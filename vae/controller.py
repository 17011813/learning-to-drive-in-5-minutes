# Orignal author: Roma Sokolkov
# VAE controller for runtime optimization.


import numpy as np

from .model import ConvVAE
from .data_loader import denormalize, preprocess_input


class VAEController:
    """
    :param z_size: (int)
    :param image_size: ((int, int, int))
    :param learning_rate: (float)
    :param kl_tolerance: (float)
    :param epoch_per_optimization: (int)
    :param batch_size: (int)
    :param buffer_size: (int)
    """
    def __init__(self, z_size=512, image_size=(80, 160, 3),
                 learning_rate=0.0001, kl_tolerance=0.5,
                 epoch_per_optimization=10, batch_size=64,
                 buffer_size=500):
        # VAE input and output shapes
        self.z_size = z_size
        self.image_size = image_size

        # VAE params
        self.learning_rate = learning_rate
        self.kl_tolerance = kl_tolerance

        # Training params
        self.epoch_per_optimization = epoch_per_optimization
        self.batch_size = batch_size

        self.vae = ConvVAE(z_size=self.z_size,
                           batch_size=self.batch_size,
                           learning_rate=self.learning_rate,
                           kl_tolerance=self.kl_tolerance,
                           is_training=True,
                           reuse=False)

        self.target_vae = ConvVAE(z_size=self.z_size,
                                  batch_size=1,
                                  is_training=False,
                                  reuse=False)

    def encode(self, arr):
        assert arr.shape == self.image_size
        # Normalize
        arr = preprocess_input(arr.astype(np.float32), mode="rl")[None]
        return self.target_vae.encode(arr)

    def decode(self, arr):
        assert arr.shape == (1, self.z_size)
        # Decode
        arr = self.target_vae.decode(arr)
        # Denormalize
        arr = denormalize(arr, mode="rl")
        return arr

    def save(self, path):
        self.target_vae.save(path)

    def load(self, path):
        self.target_vae = ConvVAE.load(path)
        self.z_size = self.target_vae.z_size

    def save_json(self, path):
        self.target_vae.save_json(path)

    def load_json(self, path):
        self.target_vae.load_json(path)

    def set_target_params(self):
        params = self.vae.get_params()
        self.target_vae.set_params(params)

    def reset_target_vae(self):
        self.target_vae = ConvVAE(z_size=self.z_size,
                                  batch_size=1,
                                  is_training=False,
                                  reuse=False)
        self.set_target_params()
