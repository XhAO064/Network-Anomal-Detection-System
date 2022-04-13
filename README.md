
# 运行代码 #
### 该项目通过 Anaconda 4.10.3配置环境 https://anaconda.org/anaconda/python ###
### Python版本为3.9 系统版本为Windows11 21H2 ###
## 以下是如何构建异常检测系统的简单教程 ##


    from AnomDetSys import *
    
    # anomalDetector params:
    maxAE = 10 #maximum size for any autoencoder in the ensemble layer
    FMgrace = 5000 #the number of instances taken to learn the feature mapping (the ensemble's architecture)
    ADgrace = 50000 #the number of instances used to train the anomaly detector (ensemble itself)
    packet_limit = np.Inf #the number of packets from the input file to process
    path = "../../captured.pcap" #the pcap, pcapng, or tsv file which you wish to process.
    
    # Build AnomDetSys
    K = AnomDetSys(path,packet_limit,maxAE,FMgrace,ADgrace)




### 输入文件可以是任何 pcap 网络数据包。 创建对象时，代码会检查您是否安装了 tshark (Wireshark)。 如果安装了，那么它使用 tshark 将 pcap 解析为一个 tsv 文件，该文件保存到本地磁盘。 然后在运行anomalDetector时使用该文件。 您还可以直接加载此 tsv 文件而不是原始 pcap 来节省时间。 请注意，tshark的默认安装路径为Windows 目录“C:\Program Files\Wireshark\tshark.exe”，如果您的安装路径与上述不同，请将代码中的tshark路径修改为您的安装路径。###
### 如果没有找到 tshark，则使用 scapy 数据包解析库。 Scapy的速度比使用 wireshark慢得多。 ###

### 要使AnomDetSys对象，只需告诉AnomDetSys处理下一个数据包。 处理完数据包后，AnomDetSys返回数据包的 RMSE 值（在 FM 特征映射和 AD 训练期间为零）。 ###

### 这是 AnonDetSys 对象的示例用法： ###

    while True: 
    	rmse = K.proc_next_packet() #will train during the grace periods, then execute on all the rest.
    	if rmse == -1:
    	break
    	print(rmse)
    


##   程序使用演示  ##
### 想要快速开始使用，test.py 中提供了一个演示脚本。 在演示中，我们在 Mirai 数据集上运行该网络异常检测系统。 你可以直接运行 ###



## 数据集下载  ##
### 测试使用的所有数据集都可以在以下网址下载 ###
### https://goo.gl/iShM7E ###



