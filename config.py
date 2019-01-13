# Raw camera input
CAMERA_HEIGHT = 120
CAMERA_WIDTH = 160
CAMERA_RESOLUTION = (CAMERA_WIDTH, CAMERA_HEIGHT)
MARGIN_TOP = CAMERA_HEIGHT // 3
# Region Of Interest
# r = [margin_left, margin_top, width, height]
ROI = [0, MARGIN_TOP, CAMERA_WIDTH, CAMERA_HEIGHT - MARGIN_TOP]

# Input dimension for VAE
IMAGE_WIDTH = ROI[2]
IMAGE_HEIGHT = ROI[3]
N_CHANNELS = 3
INPUT_DIM = (IMAGE_HEIGHT, IMAGE_WIDTH, N_CHANNELS)

# Reward parameters
THROTTLE_REWARD_WEIGHT = 0.1
JERK_REWARD_WEIGHT = 0.0

# 10% -> 0.2 diff in steering allowed
MAX_STEERING_DIFF = 0.1
# Negative reward for getting off the road
REWARD_CRASH = -10
# Penalize the agent even more when being fast
CRASH_SPEED_WEIGHT = 5

# Symmetric command
MAX_STEERING = 1
MIN_STEERING = - MAX_STEERING

# Simulation config
MIN_THROTTLE = 0.4
MAX_THROTTLE = 0.6
N_COMMAND_HISTORY = 10
# Action repeat
FRAME_SKIP = 1
Z_SIZE = 512 # Only used for random features
# No frame skip during testing
# it allows smoother control
TEST_FRAME_SKIP = 1
MAX_CTE_ERROR = 2.0
LEVEL = 0
BASE_ENV = "DonkeyVae-v0"
ENV_ID = "DonkeyVae-v0-level-{}".format(LEVEL)
SIM_PARAMS = ['MIN_THROTTLE', 'MAX_THROTTLE', 'FRAME_SKIP',
              'MAX_CTE_ERROR', 'N_COMMAND_HISTORY']

# DEBUG PARAMS
# Show input and reconstruction in the teleop panel
SHOW_IMAGES_TELEOP = False
# Show steering plots
SHOW_PLOTS = False
N_HISTORY = 200
