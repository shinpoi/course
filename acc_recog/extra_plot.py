import numpy as np
import matplotlib.pyplot as plt
import trainer as tr
import model
from chainer import using_config, no_backprop_mode, Variable, optimizers, serializers, cuda
import pickle as pk

frame_length = 40000
nfft = 110
overlap = int(nfft / 2) 

window = np.hamming(nfft)
spec_row = int((frame_length - nfft)/overlap + 1)
spec_col = int(nfft/2 + 1)
sepc_channel = 3


def spectrogram(array, channel=sepc_channel):
    data = np.zeros((spec_row, spec_col, channel), dtype=np.float64)
    for ch in range(channel):
        arr = array[:, ch]
        start = 0
        for i in range(spec_row):
            frame = arr[start: start + nfft]
            windowed = window * frame
            res = np.fft.rfft(windowed)
            # res_end = np.log(np.abs(res) ** 2)  # oringal
            res_end = np.log(np.abs(res) ** 2 + 1e0)
            data[i, :, ch] = res_end
            start += overlap
            # print(i, ch, res_end)
    return data

a = np.load("./dataset/seq_3ch_acc_NoS3/dataset_seq.npy")

data_root = "./dataset/seq_3ch_acc_NoS3/"
M = tr.Model(load_model=model.TINY_D_3ch)

serializers.load_npz(data_root + "cpu_model_end.npz", M.model)

with open(data_root + "dataflag.pkl", 'rb') as f:
    dataflag = pk.load(f)
se = tr.SeqEvaluator(M, None, dataflag)

sp_data = np.load(data_root + "seq_spec_20.npy").transpose((0, 1, 4, 2, 3))[3].reshape((1, 687, 3, 39, 56))
tr.dataflag = [dataflag[3]]
tr.detail_acc = np.zeros((6, 6), dtype=np.uint32)

se.set_seq_spec(sp_data)
eva, flagtime = se.eva_all()

eva = np.argmax(eva, axis=1)

pre_list = []
st = ed = 0
for i in range(len(eva)):
    if eva[i] == eva[st]:
        continue
    pre_list.append((st, i, eva[st]))
    st = i
    
colors = ['red', 'orange', 'green', 'blue', 'darkviolet', 'black']

plt.figure(0, figsize=(16, 9))
plt.subplot(311)
plt.title("Original Data")
plt.xlim((0,40000))
plt.xlabel("frames (1 frame = 0.01s)")
plt.ylabel("$m/s^2$")
plt.plot(range(a[3].shape[0]), a[3,:,0], color='red', label="x-axis", linewidth=0.3)
plt.plot(range(a[3].shape[0]), a[3,:,1], color='green', label="y-axis", linewidth=0.3)
plt.plot(range(a[3].shape[0]), a[3,:,2], color='blue', label="z-axis", linewidth=0.3)
plt.legend()

plt.subplot(312)
plt.title('Spectrogram')
plt.xlabel("frames (1 frame = 0.01s)")
plt.ylabel("$frequency(Hz)$")
plt.imshow(np.flip(spectrogram(a[3]).transpose((1,0,2)), 0), extent=[0, 40000, 0, 99], aspect="auto")
plt.legend()

plt.subplot(313)
plt.title("Result of Predictor")
plt.xlim(0, len(eva))
plt.ylim(0, 1)
plt.xlabel("frames (1 frame = 0.01s)")
plt.ylabel("Predict<--  -->True")

for flag in flagtime:
    plt.axvspan(flag[0], flag[1], 0.6, 0.8, facecolor=colors[flag[2]], alpha=0.6)

for flag in pre_list:
    plt.axvspan(flag[0], flag[1], 0.2, 0.4, facecolor=colors[flag[2]], alpha=0.6)

plt.plot([0],[0], color='red', label='stay')
plt.plot([0],[0], color='orange', label='walk')
plt.plot([0],[0], color='green', label='jog')
plt.plot([0],[0], color='blue', label='skip')
plt.plot([0],[0], color='darkviolet', label='stUp')
plt.plot([0],[0], color='black', label='stDown')

plt.legend()
plt.tight_layout(pad=1.0, w_pad=0.1, h_pad=1.5)
plt.savefig("123.svg")


