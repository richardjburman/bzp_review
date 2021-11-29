#%%
#functions used in Fig1 code
#created RJ Burman 28 Nov 2021

#%%
#importing libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns

#%%
group1 = np.zeros(shape=(len(data),2))
group2 = np.zeros(shape=(len(data),2))
total = np.zeros(shape=(len(data),3))

for i in range(len(data)):
    
    group = data.state[i]
    
    episodes = data.episodes[i]
    
    weight = episodes/total_episodes*200
    
    resistance = data.resistance[i]
    
    age = data.age[i]
    
    phase = data.phase[i]
    
    total[i,0] = resistance

    total[i,1] = episodes
    
    total[i,2] = episodes*resistance
           
    if group == 'developed':
        
        group1[i,0] = resistance
        
        group1[i,1] = episodes

    elif group == 'developing':
        
        group2[i,0] = resistance
        
        group2[i,1] = episodes

group1_list = np.where(group1[:,1]>0)
group1_list[0].tolist()
group1_list=group1_list[0]

group2_list = np.where(group2[:,1]>0)
group2_list[0].tolist()
group2_list=group2_list[0]

group1_f = np.zeros(shape=(len(group1_list),3))
group2_f = np.zeros(shape=(len(group2_list),3))

for i in range(len(group1_list)):
    
    index = group1_list[i]
    
    group1_f[i,0] = group1[index,0]
    group1_f[i,1] = group1[index,1]
    group1_f[i,2] = group1_f[i,0]*group1_f[i,1]
    
for i in range(len(group2_list)):
    
    index = group2_list[i]
    
    group2_f[i,0] = group2[index,0]
    group2_f[i,1] = group2[index,1]
    group2_f[i,2] = group2_f[i,0]*group2_f[i,1]
    
mean_diff_group1 = np.sum(group1_f[:,2],axis=0)/np.sum(group1_f[:,1],axis=0)*100
print(mean_diff_group1)

mean_diff_group2 = np.sum(group2_f[:,2],axis=0)/np.sum(group2_f[:,1],axis=0)*100
print(mean_diff_group2)

mean_diff_total = np.sum(total[:,2],axis=0)/np.sum(total[:,1],axis=0)*100
print(mean_diff_total)

#%%
fig,ax=plt.subplots(figsize=(5,5))

x = [.2,.3]

total_episodes = data['episodes'].sum()

freq = data['state'].value_counts()

for i in range(len(data)):
    
    group = data.state[i]
    
    episodes = data.episodes[i]
    
    weight = episodes/total_episodes*300
    
    resistance = data.resistance[i]*100
    
    age = data.age[i]
    
    if group == 'developed' and age == 'adult':
        
        ax.plot(x[0], resistance,markersize=10, color='blue', marker = 'o',alpha=.2)
   
    elif group == 'developed' and age == 'paediatric':
        
        ax.plot(x[0], resistance,markersize=10, color='blue', marker = 'o',alpha=.2)
        
    elif group == 'developed' and age == 'both':
        
        ax.plot(x[0], resistance,markersize=10, color='blue', marker = 'o',alpha=.2)        

    elif group == 'developing' and age == 'adult':
        
        ax.plot(x[1], resistance,markersize=10, color='red', marker = 'o',alpha=.2)

    elif group == 'developing' and age == 'paediatric':
        
        ax.plot(x[1], resistance,markersize=10, color='red', marker = 'o',alpha=.2)       
        
    elif group == 'developing' and age == 'both':
        
        ax.plot(x[1], resistance,markersize=10, color='red', marker = 'o',alpha=.2)        
        
plt.xlim(.1,.4)

ax.set_xticks(x)

labels = ['developed','developing']

ax.set_xticklabels(labels)

ax.set_ylabel('BZP-R (%)')

ax.plot(x[0],mean_diff_group1, markersize=15, color='blue', marker = 'o')
ax.plot(x[1],mean_diff_group2, markersize=15, color='red', marker = 'o')
#ax.plot(.25,mean_diff_total, markersize=15, color='black', marker = 'o')

#ax.plot(.125,73,markersize=10,marker='*',color='black')
#plt.text(.140, 71, 'Mean diff.', fontsize=12)

#ax.axhline(mean_diff_total, linewidth=1, linestyle='--', color = 'black')

os.chdir(r'C:\Users\rburman.MSDITUN-TMV0GCR\OneDrive - Nexus365\Code\bzp_review\Fig 1')
fig.savefig('Fig1A' + '.png', format='png')
fig.savefig('Fig1A' + '.eps', format='eps')

#%%
total_episodes = data['episodes'].sum()

freq = data['state'].value_counts()

phase1 = np.zeros(shape=(len(data),2))
phase2 = np.zeros(shape=(len(data),2))
phase3 = np.zeros(shape=(len(data),2))

for i in range(len(data)):
    
    group = data.state[i]
    
    episodes = data.episodes[i]
    
    weight = episodes/total_episodes*500
    
    resistance = data.resistance[i]
    
    age = data.age[i]
    
    phase = data.phase[i]
           
    if phase == '10-30min':
        
        phase1[i,0] = resistance
        
        phase1[i,1] = episodes

    elif phase == '31-60min':
        
        phase2[i,0] = resistance
        
        phase2[i,1] = episodes

    elif phase == '>60min':
        
        phase3[i,0] = resistance
        
        phase3[i,1] = episodes

phase1_list = np.where(phase1[:,1]>0)
phase1_list[0].tolist()
phase1_list=phase1_list[0]

phase2_list = np.where(phase2[:,1]>0)
phase2_list[0].tolist()
phase2_list=phase2_list[0]

phase3_list = np.where(phase3[:,1]>0)
phase3_list[0].tolist()
phase3_list=phase3_list[0]

phase1_f = np.zeros(shape=(len(phase1_list),3))
phase2_f = np.zeros(shape=(len(phase2_list),3))
phase3_f = np.zeros(shape=(len(phase3_list),3))

for i in range(len(phase1_list)):
    
    index = phase1_list[i]
    
    phase1_f[i,0] = phase1[index,0]
    phase1_f[i,1] = phase1[index,1]
    phase1_f[i,2] = phase1_f[i,0]*phase1_f[i,1]
    
for i in range(len(phase2_list)):
    
    index = phase2_list[i]
    
    phase2_f[i,0] = phase2[index,0]
    phase2_f[i,1] = phase2[index,1]
    phase2_f[i,2] = phase2_f[i,0]*phase2_f[i,1]
    
for i in range(len(phase3_list)):
    
    index = phase3_list[i]
    
    phase3_f[i,0] = phase3[index,0]
    phase3_f[i,1] = phase3[index,1]
    phase3_f[i,2] = phase3_f[i,0]*phase3_f[i,1]    
    
mean_diff_phase1 = np.sum(phase1_f[:,2],axis=0)/np.sum(phase1_f[:,1],axis=0)*100
print(mean_diff_phase1)

mean_diff_phase2 = np.sum(phase2_f[:,2],axis=0)/np.sum(phase2_f[:,1],axis=0)*100
print(mean_diff_phase2)

mean_diff_phase3 = np.sum(phase3_f[:,2],axis=0)/np.sum(phase3_f[:,1],axis=0)*100
print(mean_diff_phase3)