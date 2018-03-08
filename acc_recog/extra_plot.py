import numpy as np
import matplotlib.pyplot as plt
import trainer as tr
import model
from chainer import using_config, no_backprop_mode, Variable, optimizers, serializers, cuda
import pickle as pk
import os

I = 14
CH = 6
data_root = "./dataset/"

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


dataset = np.load(data_root + "dataset_seq.npy")
a = dataset
# M = tr.Model(load_model=model.TINY_D_3ch)
M = tr.Model(load_model=model.TINY_D_6ch, load_data=False)
serializers.load_npz(data_root + "cpu_model_end.npz", M.model)

with open(data_root + "dataflag.pkl", 'rb') as f:
    dataflag = pk.load(f)
lim = dataflag[I][-1][1]
se = tr.SeqEvaluator(M, dataset, dataflag)

# sp_data = np.load(data_root + "seq_spec_20.npy").transpose((0, 1, 4, 2, 3))[I].reshape((1, 687, CH, 39, 56))
# tr.dataflag = [dataflag[I]]
tr.detail_acc = np.zeros((6, 6), dtype=np.uint32)

# se.set_seq_spec(sp_data)
eva_list, flagtime = se.eva_all()
ac = tr.detail_acc
print(ac)
print("acc = %f" % (np.sum([ac[i, i] for i in range(ac.shape[0])]) / np.sum(ac)))
print("recall: ", [ac[i,i]/np.sum(ac[i]) for i in range(ac.shape[0])])
print("precision: ", [ac[i,i]/np.sum(ac[:, i]) for i in range(ac.shape[0])])

eva_list = np.argmax(eva_list, axis=2)

pre_list = []
for eva in eva_list:
    st = ed = 0
    temp_list = []
    for i in range(len(eva)):
        if eva[i] == eva[st]:
            continue
        temp_list.append((st, i, eva[st]))
        st = i
    temp_list.append((st, len(eva)-1, eva[-1]))
    pre_list.append(temp_list)

colors = ['red', 'orange', 'green', 'blue', 'darkviolet', 'black']

try:
    os.mkdir(data_root + "plot")
except FileExistsError:
    pass

print("plot start ...")
for i in range(len(eva_list)):
    plt.figure(0, figsize=(16, 9))
    plt.subplot(311)
    plt.title("Original Data")
    plt.xlim((0,lim))
    plt.xlabel("frames (1 frame = 0.01s)")
    plt.ylabel("$m/s^2$")
    plt.plot(range(a[i].shape[0]), a[i,:,0], color='red', label="x-axis", linewidth=0.3)
    plt.plot(range(a[i].shape[0]), a[i,:,1], color='green', label="y-axis", linewidth=0.3)
    plt.plot(range(a[i].shape[0]), a[i,:,2], color='blue', label="z-axis", linewidth=0.3)
    plt.legend()

    plt.subplot(312)
    plt.title('Spectrogram')
    plt.xlabel("frames (1 frame = 0.01s)")
    plt.ylabel("$frequency(Hz)$")
    plt.xlim((0,lim))
    plt.imshow(np.flip(spectrogram(a[i]).transpose((1,0,2)), 0), extent=[0, 40000, 0, 99], aspect="auto")
    # plt.legend()

    plt.subplot(313)
    plt.title("Result of Predictor")
    plt.xlim(0, int(len(eva)*(lim/40000)))
    plt.ylim(0, 1)
    plt.xlabel("frames (1 frame = 0.55s)")
    plt.ylabel("Predict<--  -->True")

    for flag in flagtime[i]:
        plt.axvspan(flag[0], flag[1], 0.6, 0.8, facecolor=colors[flag[2]], alpha=0.6)

    for flag in pre_list[i]:
        plt.axvspan(flag[0], flag[1], 0.2, 0.4, facecolor=colors[flag[2]], alpha=0.6)

    plt.plot([0],[0], color='red', label='stay')
    plt.plot([0],[0], color='orange', label='walk')
    plt.plot([0],[0], color='green', label='jog')
    plt.plot([0],[0], color='blue', label='skip')
    plt.plot([0],[0], color='darkviolet', label='stUp')
    plt.plot([0],[0], color='black', label='stDown')

    plt.legend()
    plt.tight_layout(pad=1.0, w_pad=0.1, h_pad=1.5)
    plt.savefig(data_root + "plot/%d.svg" % i)
    plt.close(0)
