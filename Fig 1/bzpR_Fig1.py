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
from scipy import stats


#%%

def fig1A(data):

    total_episodes = data['episodes'].sum()

    hic = np.zeros(shape=(len(data),2))
    lmic = np.zeros(shape=(len(data),2))
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
            
        if group == 'high-income':
            
            hic[i,0] = resistance
            
            hic[i,1] = episodes

        elif group == 'low-middle-income':
            
            lmic[i,0] = resistance
            
            lmic[i,1] = episodes

    hic_list = np.where(hic[:,1]>0)
    hic_list[0].tolist()
    hic_list=hic_list[0]

    lmic_list = np.where(lmic[:,1]>0)
    lmic_list[0].tolist()
    lmic_list=lmic_list[0]

    hic_final = np.zeros(shape=(len(hic_list),3))
    lmic_final = np.zeros(shape=(len(lmic_list),3))

    for i in range(len(hic_list)):
        
        index = hic_list[i]
        
        hic_final[i,0] = hic[index,0]
        hic_final[i,1] = hic[index,1]
        hic_final[i,2] = hic_final[i,0]*hic_final[i,1]
        
    for i in range(len(lmic_list)):
        
        index = lmic_list[i]
        
        lmic_final[i,0] = lmic[index,0]
        lmic_final[i,1] = lmic[index,1]
        lmic_final[i,2] = lmic_final[i,0]*lmic_final[i,1]

    #calculating mean and weighted mean difference between economic groups
    
    mean_hic = np.mean(hic_final[:,0])*100

    mean_lmic = np.mean(lmic_final[:,0])*100

    mean_total = np.mean(total[:,0])*100

    mean_diff_hic = np.sum(lmic_final[:,2],axis=0)/np.sum(lmic_final[:,1],axis=0)*100
    
    mean_diff_lmic = np.sum(lmic_final[:,2],axis=0)/np.sum(lmic_final[:,1],axis=0)*100

    mean_diff_total = np.sum(total[:,2],axis=0)/np.sum(total[:,1],axis=0)*100 

    #working out ditribution of resistance values
    shapiro_data1 = stats.shapiro(lmic_final[:,2])
    shapiro_data2 = stats.shapiro(hic_final[:,2])

    #perfomring comparative statistics based on the the distribution of the resistance values
    if shapiro_data1 or shapiro_data2 >0.05:
        p_value = stats.ttest_ind(lmic_final[:,0],hic_final[:,0])
        test = 'unpaired t-test'

    elif shapiro_data1 or shapiro_data2 <0.05:
        p_value = stats.mannwhitneyu(lmic_final[:,0],hic_final[:,0])
        test = 'mann-whitney'   
   
    #plotting new figure which collapses data to separate only between economic groups

    Fig1A,ax=plt.subplots(figsize=(5,5))

    plt.title('Fig1A')

    x = [.2,.3]

    total_episodes = data['episodes'].sum()

    freq = data['state'].value_counts()

    for i in range(len(data)):
        
        group = data.state[i]
        
        episodes = data.episodes[i]
        
        weight = episodes/total_episodes*300
        
        resistance = data.resistance[i]*100
        
        age = data.age[i]
        
        if group == 'high-income' and age == 'adult':
            
            ax.plot(x[0], resistance,markersize=10, color='blue', marker = 'o',alpha=.2)
    
        elif group == 'high-income' and age == 'paediatric':
            
            ax.plot(x[0], resistance,markersize=10, color='blue', marker = 'o',alpha=.2)
            
        elif group == 'high-income' and age == 'both':
            
            ax.plot(x[0], resistance,markersize=10, color='blue', marker = 'o',alpha=.2)        

        elif group == 'low-middle-income' and age == 'adult':
            
            ax.plot(x[1], resistance,markersize=10, color='red', marker = 'o',alpha=.2)

        elif group == 'low-middle-income' and age == 'paediatric':
            
            ax.plot(x[1], resistance,markersize=10, color='red', marker = 'o',alpha=.2)       
            
        elif group == 'low-middle-income' and age == 'both':
            
            ax.plot(x[1], resistance,markersize=10, color='red', marker = 'o',alpha=.2)        
            
    plt.xlim(.1,.4)

    ax.set_xticks(x)

    labels = ['HIC','LMIC']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')

    ax.plot(x[0],mean_hic, markersize=15, color='blue', marker = 'o')
    ax.plot(x[1],mean_lmic, markersize=15, color='red', marker = 'o')
    ax.plot(.25,mean_total, markersize=15, color='black', marker = 'o')

    #ax.plot(.125,73,markersize=10,marker='*',color='black')
    #plt.text(.140, 71, 'Mean diff.', fontsize=12)

    #ax.axhline(mean_total, linewidth=1, linestyle='--', color = 'black')

    axes_limits = ax.get_ylim()

    ax.plot([x[0],x[1]],[axes_limits[1],axes_limits[1]],color='black', lw=1)

    posOne = x[1]-(x[1]-x[0])+(x[1]-x[0])/4

    p = 'p = ' + str(np.round(p_value[1],2))

    font_size = 10

    ax.annotate(p,(posOne,axes_limits[1]+.5),color = 'black',fontsize=font_size)

    plt.close(Fig1A)

    #plotting original figure with all detail (i.e. stratified across economic groups, ages and weighted according to sample size)

    SuppFig1A,ax=plt.subplots(figsize=(5,5))

    plt.title('SuppFig1A')

    x = [.2,.3]

    for i in range(len(data)):
    
        group = data.state[i]
    
        episodes = data.episodes[i]
    
        weight = episodes/total_episodes*300
    
        resistance = data.resistance[i]*100
    
        age = data.age[i]
    
        if group == 'high-income' and age == 'adult':
        
            ax.plot(x[0]-.015, resistance,markersize=weight, color='blue', marker = 'o',alpha=.2)
   
        elif group == 'high-income' and age == 'paediatric':
        
            ax.plot(x[0]+.015, resistance,markersize=weight, color='magenta', marker = 'o',alpha=.2)
        
        elif group == 'high-income' and age == 'both':
        
            ax.plot(x[0], resistance,markersize=weight, color='black', marker = 'o',alpha=.2)        

        elif group == 'low-middle-income' and age == 'adult':
        
            ax.plot(x[1]-.015, resistance,markersize=weight, color='blue', marker = 'o',alpha=.2)

        elif group == 'low-middle-income' and age == 'paediatric':
        
            ax.plot(x[1]+.015, resistance,markersize=weight, color='magenta', marker = 'o',alpha=.2)       
        
        elif group == 'low-middle-income' and age == 'both':
        
            ax.plot(x[1], resistance,markersize=weight, color='black', marker = 'o',alpha=.2)        
        
    plt.xlim(.1,.4)

    ax.set_xticks(x)

    labels = ['HIC','LMIC']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')

    ax.plot(x[0],mean_diff_hic, markersize=15, color='blue', marker = 'o')
    ax.plot(x[1],mean_diff_lmic, markersize=15, color='red', marker = 'o')
    ax.plot(.25,mean_diff_total, markersize=15, color='black', marker = 'o')

    ax.plot(.125,88,markersize=10,marker='o',color='blue',alpha=.2)
    plt.text(.140, 86, 'Adult only', fontsize=12)

    ax.plot(.125,83,markersize=10,marker='o',color='black',alpha=.2)
    plt.text(.140, 81, 'Mixed', fontsize=12)

    ax.plot(.125,78,markersize=10,marker='o',color='magenta',alpha=.2)
    plt.text(.140, 76, 'Paediatric only', fontsize=12)

    plt.close(SuppFig1A)

    return(mean_hic, mean_lmic, mean_total, p_value, test, Fig1A,  mean_diff_hic, mean_diff_lmic, mean_diff_total, SuppFig1A)

#%%

def fig1B(data):

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

    #plotting new figure which separates across SE duration between economic groups

    Fig1B,ax=plt.subplots(figsize=(5,5))

    x = [.2,.3,.4]

    total_episodes = data['episodes'].sum()

    freq = data['state'].value_counts()

    phase1 = np.zeros(shape=(len(data),2))
    phase2 = np.zeros(shape=(len(data),2))
    phase3 = np.zeros(shape=(len(data),2))

    for i in range(len(data)):
        
        group = data.state[i]
        
        episodes = data.episodes[i]
        
        weight = 10
        
        resistance = data.resistance[i]*100
        
        age = data.age[i]
        
        phase = data.phase[i]
        
        marker = 'o'
           
        if phase == '10-30min' and group == 'high-income':
            
            phase1[i,0] = resistance
            
            phase1[i,1] = episodes
            
            ax.plot(x[0]-.015, resistance,markersize=weight, color = 'blue', marker = marker, alpha=.2)

        elif phase == '10-30min' and group == 'low-middle-income':
            
            phase1[i,0] = resistance
            
            phase1[i,1] = episodes
            
            ax.plot(x[0]+.015, resistance,markersize=weight, color = 'red', marker = marker, alpha=.2)
        
        elif phase == '31-60min' and group == 'high-income':
            
            phase2[i,0] = resistance
            
            phase2[i,1] = episodes
            
            ax.plot(x[1]-.015, resistance,markersize=weight, color = 'blue', marker = marker,alpha=.2)        

        elif phase == '31-60min' and group == 'low-middle-income':
            
            phase2[i,0] = resistance
            
            phase2[i,1] = episodes
            
            ax.plot(x[1]+.015, resistance,markersize=weight, color = 'red', marker = marker,alpha=.2)               
            
        elif phase == '>60min' and group == 'high-income':
            
            phase3[i,0] = resistance
            
            phase3[i,1] = episodes
            
            ax.plot(x[2]-.015, resistance,markersize=weight, color = 'blue', marker = marker, alpha=.2)        

        elif phase == '>60min' and group == 'low-middle-income':
            
            phase3[i,0] = resistance
            
            phase3[i,1] = episodes
            
            ax.plot(x[2]+.015, resistance,markersize=weight, color = 'red', marker = marker, markeredgewidth=2, alpha=.2)        
            
    ax.plot(x[0],mean_diff_phase1, markersize=15, color='purple', marker = 'o')
    ax.plot(x[1],mean_diff_phase2, markersize=15, color='purple', marker = 'o')
    ax.plot(x[2],mean_diff_phase3, markersize=15, color='purple', marker = 'o')
            
    plt.xlim(.1,.5)

    ax.set_xticks(x)

    labels = ['10-30min','31-60min','>60min']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')

    #plotting original figure with all detail (i.e. stratified across duration of SE, age of participants, number of participants and economic groups)
      
    SuppFig1B,ax=plt.subplots(figsize=(5,5))

    x = [.2,.3,.4]

    total_episodes = data['episodes'].sum()

    freq = data['state'].value_counts()

    phase1 = np.zeros(shape=(len(data),2))
    phase2 = np.zeros(shape=(len(data),2))
    phase3 = np.zeros(shape=(len(data),2))

    for i in range(len(data)):
        
        group = data.state[i]
        
        episodes = data.episodes[i]
        
        weight = episodes/total_episodes*500
        
        resistance = data.resistance[i]*100
        
        age = data.age[i]
        
        phase = data.phase[i]
        
        marker = 'o'
        
        if age == 'paediatric':
            
            color = 'magenta'

        elif age == 'adult':
            
            color = 'blue'

        elif age == 'both':
            
            color = 'black'           

    #    if group == 'developed':
            
    #        color = 'blue'

    #    elif group == 'developing':
            
    #        color = 'magenta'     
            
        if phase == '10-30min' and group == 'high-income':
            
            phase1[i,0] = resistance
            
            phase1[i,1] = episodes
            
            ax.plot(x[0]-.015, resistance,markersize=weight, color = color, marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)

        elif phase == '10-30min' and group == 'low-middle-income':
            
            phase1[i,0] = resistance
            
            phase1[i,1] = episodes
            
            ax.plot(x[0]+.015, resistance,markersize=weight, color = color, marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)
        
        elif phase == '31-60min' and group == 'high-income':
            
            phase2[i,0] = resistance
            
            phase2[i,1] = episodes
            
            ax.plot(x[1]-.015, resistance,markersize=weight, color = color, marker = marker, markeredgecolor = color, markeredgewidth=2,alpha=.2)        

        elif phase == '31-60min' and group == 'low-middle-income':
            
            phase2[i,0] = resistance
            
            phase2[i,1] = episodes
            
            ax.plot(x[1]+.015, resistance,markersize=weight, color = color, marker = marker, markeredgecolor = color, markeredgewidth=2,alpha=.2)               
            
        elif phase == '>60min' and group == 'high-income':
            
            phase3[i,0] = resistance
            
            phase3[i,1] = episodes
            
            ax.plot(x[2]-.015, resistance,markersize=weight, color = color, marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)        

        elif phase == '>60min' and group == 'low-middle-income':
            
            phase3[i,0] = resistance
            
            phase3[i,1] = episodes
            
            ax.plot(x[2]+.015, resistance,markersize=weight, color = color, marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)        
            
    ax.plot(x[0],mean_diff_phase1, markersize=15, color='black', marker = 'o')
    ax.plot(x[1],mean_diff_phase2, markersize=15, color='black', marker = 'o')
    ax.plot(x[2],mean_diff_phase3, markersize=15, color='black', marker = 'o')
            
    plt.xlim(.1,.5)

    ax.set_xticks(x)

    labels = ['10-30min','31-60min','>60min']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')

    ax.plot(.125,80,markersize=10,marker='o',color='blue',alpha=.2)
    plt.text(.140, 78, 'Adult only', fontsize=12)
    ax.plot(.125,75,markersize=10,marker='o',color='magenta',alpha=.2)
    plt.text(.140, 73, 'Paediatric only', fontsize=12)
    ax.plot(.125,70,markersize=10,marker='o',color='black',alpha=.2)
    plt.text(.140, 68, 'Mixed', fontsize=12)
    #ax.plot(.125,65,markersize=10,marker='*',color='black')
    #plt.text(.140, 63, 'Mean diff.', fontsize=12)
    #ax.plot(.125,60,markersize=10,marker='_',color='blue')
    #plt.text(.140, 58, 'Developed', fontsize=12)
    #ax.plot(.125,55,markersize=10,marker='_',color='magenta')
    #plt.text(.140, 53, 'Developing', fontsize=12)

    return(Fig1B, SuppFig1B)
