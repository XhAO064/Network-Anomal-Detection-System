from AnomDetSys import AnomDetSys
import numpy as np
import time
import pandas as pd

# Load Mirai pcap (a recording of the Mirai botnet malware being activated)
# The first 70,000 observations are clean...

# 正态分布函数 x为数据中的某一具体测量值，mu为均值，sigma为方差
def normfun(x,mu,sigma):
    pdf= np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf
#
print("Unzipping Sample Capture...")



# File location
path = "mirai.pcap" #the pcap, pcapng, or tsv file to process.
packet_limit = np.inf #the number of packets to process
# AnomDetc params:
maxAE = 10 #maximum size for any autoencoder in the ensemble layer
FMgrace = 5000 #the number of instances taken to learn the feature mapping (the ensemble's architecture)
ADgrace = 50000 #the number of instances used to train the anomaly detector (ensemble itself)

# Build AnomDetSys
ADS = AnomDetSys(path, packet_limit, maxAE, FMgrace, ADgrace)

print("Running AnomDetSys:")
RMSEs = []
i = 0
#
# threshold=-1
#
start = time.time()
# Here we process (train/execute) each individual packet.
# In this way, each observation is discarded after performing process() method.
while True:
    i+=1
    if i % 10000 == 0:
        print(i)
    rmse = ADS.proc_next_packet()
    if rmse == -1:
        break

    RMSEs.append(rmse)

    if rmse>4496:
        print("第"+str(i)+"条数据可能为异常")
#
# mean=np.mean(RMSEs[FMgrace+ADgrace:])
# std=np.std(RMSEs[FMgrace+ADgrace:])
# x=np.arange(0,4600,0.1)
# y=normfun(x,mean,std)
#
# print("rmse最大为"+str(max(RMSEs)))
stop = time.time()
print("Complete. Time elapsed: "+ str(stop - start))


# Here we demonstrate how one can fit the RMSE scores to a log-normal distribution (useful for finding/setting a cutoff threshold \phi)
from scipy.stats import norm
benignSample = np.log(RMSEs[FMgrace+ADgrace+1:100000])
logProbs = norm.logsf(np.log(RMSEs), np.mean(benignSample), np.std(benignSample))

# plot the RMSE anomaly scores
print("Plotting results")
from matplotlib import pyplot as plt
from matplotlib import cm
plt.figure(figsize=(10,5))
fig = plt.scatter(range(FMgrace+ADgrace+1,len(RMSEs)),RMSEs[FMgrace+ADgrace+1:],s=0.1,c=logProbs[FMgrace+ADgrace+1:],cmap='RdYlGn')
plt.yscale("log")
plt.title("Anomaly Scores from Execution Phase")
plt.ylabel("RMSE (log scaled)")
plt.xlabel("Time elapsed [min]")
figbar=plt.colorbar()
figbar.ax.set_ylabel('Log Probability\n ', rotation=270)
plt.show()

# #绘制数据集的整体分布曲线
# plt.figure(figsize=(10,5))
# plt.plot(x,y)
# #绘制直方图
# plt.hist(RMSEs,bins=15000,density=True,log=True)
# plt.title("distribution")
# plt.xlabel("rmse")
# plt.show()
