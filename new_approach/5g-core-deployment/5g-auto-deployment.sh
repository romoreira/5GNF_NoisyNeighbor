#!/bin/bash

#echo "Installing deps"
#sudo apt-get install gcc make
#echo "Building GPT"
#git clone -b v0.8.2 https://github.com/free5gc/gtp5g.git
#cd /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/gtp5g/
#echo "####Uninstalling previous GPT versions"
#sudo make uninstall
#make clean && make
#sudo make install

echo "###Deleting previous deployment###"
kubectl delete deployment ueransim-gnb --force
kubectl delete deployment ueransim-ue1 --force
kubectl delete deployment free5gc-smf --force
#kubectl delete deployment free5gc-upf --force
kubectl delete deployment free5gc-amf --force
kubectl delete deployment free5gc-ausf --force
#kubectl delete deployment free5gc-nrf --force
kubectl delete deployment free5gc-nssf --force
kubectl delete deployment free5gc-pcf --force
kubectl delete deployment free5gc-udm --force
kubectl delete deployment free5gc-udr --force
kubectl delete pod test-my5g --force
sleep 30

echo "\nBuilding network script\n"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/networks5g/network-attachments-ovs.yaml
echo "\nBuilding DB\n"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deploymentfree5gc-k8s/mongodb/mongodb-serviceaccount.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/mongodb/mongodb-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/mongodb/mongodb-deployment.yaml
echo "\nBuilding free5GC GUI\n"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc-webui/webui-configmap.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc-webui/webui-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc-webui/webui-deployment.yaml
echo "\nBuilding 5G core entities\n"
sleep 120
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/amf/amf-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/amf/amf-configmap.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/amf/amf-deployment.yaml
sleep 120
echo "###Building AUSF###"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/ausf/ausf-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/ausf/ausf-configmap.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/ausf/ausf-deployment.yaml
sleep 120
echo "###Building NRF###"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/nrf/nrf-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/nrf/nrf-configmap.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/nrf/nrf-deployment.yaml
sleep 120
echo "Builing SMF"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/slices/slice1/smf1/smf-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/slices/slice1/smf1/smf-configmap.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/slices/slice1/smf1/smf-deployment.yaml
sleep 120
echo "###Building PCF###"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/pcf/pcf-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/pcf/pcf-configmap.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/pcf/pcf-deployment.yaml
sleep 120
echo "###Building UDM###"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/udm/udm-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/udm/udm-configmap.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/udm/udm-deployment.yaml
sleep 120
echo "###Building UDR###"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/udr/udr-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/udr/udr-configmap.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/udr/udr-deployment.yaml
sleep 120
echo "###Building NSSF###"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/nssf/nssf-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/nssf/nssf-configmap.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/common/nssf/nssf-deployment.yaml
sleep 120
echo "Building GNB"
kubectl create configmap gnb-configmap --from-file=/home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/ueransim/ueransim-gnb/config/free5gc-gnb.yaml --from-file=/home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/ueransim/ueransim-gnb/config/wrapper.sh
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/ueransim/ueransim-gnb/gnb-service.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/ueransim/ueransim-gnb/gnb-deployment.yaml
sleep 120
echo "Builing UPF"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/slices/slice1/upf1/upf-configmap.yaml
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/free5gc/slices/slice1/upf1/upf-deployment.yaml
sleep 120
echo "Building Workload Generation POD"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/ubuntu.yaml
sleep 120
echo "Building UE"
#kubectl create configmap ue1-configmap --from-file=/home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/ueransim/ueransim-ue/ue1/ue1.yaml --from-file=/home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/ueransim/ueransim-ue/ue1/wrapper.sh
kubectl create configmap ue1-configmap --from-file=ue1.yaml --from-file=ue-cfg.yaml --from-file=wrapper.sh
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/free5gc-k8s/ueransim/ueransim-ue/ue1/deployment.yaml
echo "Building my-5gtester"
kubectl apply -f /home/lab-manager/PychgarmProjects/5GNF_NoisyNeighbor/new_approach/5g-core-deployment/NetAIAPP-AnomalyDetection/free5GC-benchmark/test-my5g-pod-deployment/ubuntu-pod-deployment.yaml