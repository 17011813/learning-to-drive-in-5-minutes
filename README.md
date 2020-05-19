# Learning to Drive Smoothly in Minutes

Learning to drive smoothly in minutes, using a reinforcement learning algorithm -- Soft Actor-Critic (SAC) -- and a Variational AutoEncoder (VAE) in the Donkey Car simulator.


Blog post on Medium: [link](https://medium.com/@araffin/learning-to-drive-smoothly-in-minutes-450a7cdb35f4)

Video: [https://www.youtube.com/watch?v=iiuKh0yDyKE](https://www.youtube.com/watch?v=iiuKh0yDyKE)


Level-0          | Level-1
:-------------------------:|:-------------------------:
![result](content/smooth.gif)  | ![result](content/level1.gif)
[Download VAE](https://drive.google.com/open?id=1n7FosFA0hALhuESf1j1yg-hERCnfVc4b) |  [Download VAE](https://drive.google.com/open?id=1hfQNAvVp2QmbmTLklWt2MxtAjrlisr2B)
[Download pretrained agent](https://drive.google.com/open?id=10Hgd5BKfn1AmmVdLlNcDll6yXqVkujoq) | [Download pretrained agent](https://drive.google.com/open?id=104tlsIrtOTVxJ1ZLoTpBDzK4-DRTA5et)

Note: pretrained agents는 `logs/sac/` 폴더에 넣어주어야 합니다. 없으면 생성! (you need to pass `--exp-id 6` (index of the folder) to use the pretrained agent). 그리고 VAE Level 0, VAE Level 1은 `logs` 폴더에 넣어줍니다.

저는 기본 python이 2.7이 깔려있어 python3로 pip3를 사용하여 진행하였습니다.
## Quick Start
저는 리눅스 환경에서 진행하였습니다.
0. Download simulator [here](https://drive.google.com/open?id=1h2VfpGHlZetL5RAPZ79bhDRkvlfuB4Wb) or build it from [source](https://github.com/tawnkramer/sdsandbox/tree/donkey)
1. Install dependencies (pip3 install -r requirements.txt)
2. (optional but recommended) Download pre-trained VAE: [VAE Level 0](https://drive.google.com/open?id=1n7FosFA0hALhuESf1j1yg-hERCnfVc4b) [VAE Level 1](https://drive.google.com/open?id=1hfQNAvVp2QmbmTLklWt2MxtAjrlisr2B)
3. Train a control policy for 5000 steps using Soft Actor-Critic (SAC)

```
python3 train.py --algo sac -vae path-to-vae.pkl -n 5000
```
위의 path-to-vae.pkl 의 경우 VAE 0 미리 다운받은 거로 하려면 logs/vae-level-0-dim-32.pkl로 설정해주면 됩니다.

4. Enjoy trained agent for 2000 steps

```
python3 enjoy.py --algo sac -vae path-to-vae.pkl --exp-id 0 -n 2000
```
위의 path-to-vae.pkl 의 경우 VAE 0 미리 다운받은 거로 하려면 logs/vae-level-0-dim-32.pkl로 설정해주면 됩니다.

To train on a different level, you need to change `LEVEL = 0` to `LEVEL = 1` in `config.py`

## Train the Variational AutoEncoder (VAE)
여기서부터는 처음부터 직접 하는 방법입니다.
0. Collect images using the teleoperation mode:
첫번째 단계로 원격 조종모드 방향키로 직접 운전하며 도로 image를 충분히 모은다.(space bar로 녹화모드 변경 가능) 맵을 한번 이상 완주하며 충분히 모아주세요.
```
python3 -m teleop.teleop_client --record-folder path-to-record/folder/
```

1. Train a VAE:
위에서 모은 image를 이용해서 VAE 모델에 넣어서 학습시킵니다. 2시간 정도 걸립니다.
```
python3 -m vae.train --n-epochs 50 --verbose 0 --z-size 64 -f path-to-record/folder/
```

## Train in Teleoparation Mode
위의 코드까지 마치면 logs폴더에 vae.pkl이 생성됩니다.
```
python3 train.py --algo sac -vae logs/vae.pkl -n 5000 --teleop
```

## Test in Teleoparation Mode
여기서 --exp-id는 여러개의 폴더 중에 0번째 폴더안의 vae버전을 사용하겠다는 뜻입니다. 나중에 여러번 학습을 해 vae.pkl이 6번째 폴더까지 있고 6번째 폴더안의 vae.pkl을 사용하고 싶다면 --exp-id 6이라고 써주면 됩니다.

근데 저는 원래 올라와있는 이 코드 말고
```
python3 -m teleop.teleop_client --algo sac -vae logs/vae.pkl --exp-id 0
```
우선 저는 다운 받은 pretrained agent는 위의 폴더에 그냥 그대로 두고 logs폴더에 있는 vae-level-0-dim-32.pkl을 연결해주어야 에러 없이 잘 진행됩니다.
```
python3 -m teleop.teleop_client --algo sac -vae logs/vae-level-0-dim-32.pkl --exp-id 0
```

## Explore Latent Space
코드 실행 시 latent 이미지가 나옵니다.
```
python3 -m vae.enjoy_latent -vae logs/level-0/vae-8.pkl
```

## Reproducing Results

To reproduce the results shown in the video, you have to check different values in `config.py`.

### Level 0

`config.py`:

```python
MAX_STEERING_DIFF = 0.15 # 0.1 for very smooth control, but it requires more steps
MAX_THROTTLE = 0.6 # MAX_THROTTLE = 0.5 is fine, but we can go faster
MAX_CTE_ERROR = 2.0 # only used in normal mode, set it to 10.0 when using teleoperation mode
LEVEL = 0
```

Train in normal mode (smooth control), it takes ~5-10 minutes:
```
python train.py --algo sac -n 8000 -vae logs/vae-level-0-dim-32.pkl
```

Train in normal mode (very smooth control with `MAX_STEERING_DIFF = 0.1`), it takes ~20 minutes:
```
python train.py --algo sac -n 20000 -vae logs/vae-level-0-dim-32.pkl
```

Train in teleoperation mode (`MAX_CTE_ERROR = 10.0`), it takes ~5-10 minutes:
```
python train.py --algo sac -n 8000 -vae logs/vae-level-0-dim-32.pkl --teleop
```

### Level 1

Note: only teleoperation mode is available for level 1

`config.py`:

```python
MAX_STEERING_DIFF = 0.15
MAX_THROTTLE = 0.5 # MAX_THROTTLE = 0.6 can work but it's harder to train due to the sharpest turn
LEVEL = 1
```

Train in teleoperation mode, it takes ~10 minutes:
```
python train.py --algo sac -n 15000 -vae logs/vae-level-1-dim-64.pkl --teleop
```

Note: although the size of the VAE is different between level 0 and 1, this is not an important factor.

## Record a Video of the on-board camera

You need a trained model. For instance, for recording 1000 steps with the last trained SAC agent:
```
python -m utils.record_video --algo sac --vae-path logs/level-0/vae-32-2.pkl -n 1000
```

## Citing the Project

To cite this repository in publications:

```
@misc{drive-smoothly-in-minutes,
  author = {Raffin, Antonin and Sokolkov, Roma},
  title = {Learning to Drive Smoothly in Minutes},
  year = {2019},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/araffin/learning-to-drive-in-5-minutes/}},
}
```

## Credits

Related Paper: ["Learning to Drive in a Day"](https://arxiv.org/pdf/1807.00412.pdf).

- [r7vme](https://github.com/r7vme/learning-to-drive-in-a-day) Author of the original implementation
- [Wayve.ai](https://wayve.ai) for idea and inspiration.
- [Tawn Kramer](https://github.com/tawnkramer) for Donkey simulator and Donkey Gym.
- [Stable-Baselines](https://github.com/hill-a/stable-baselines) for DDPG/SAC and PPO implementations.
- [RL Baselines Zoo](https://github.com/araffin/rl-baselines-zoo) for training/enjoy scripts.
- [S-RL Toolbox](https://github.com/araffin/robotics-rl-srl) for the data loader
- [Racing robot](https://github.com/sergionr2/RacingRobot) for the teleoperation
- [World Models Experiments](https://github.com/hardmaru/WorldModelsExperiments) for VAE implementation.
