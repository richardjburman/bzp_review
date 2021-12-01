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
    shapiro_data1 = stats.shapiro(lmic_final[:,0])
    shapiro_data2 = stats.shapiro(hic_final[:,0])

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

# function to plot data of BZP-R across different reported SE durations and stratified across (i) economic area, (ii) age group of participants and (iii) number of study participants
# plot1: collapses variables to focus on difference in reported BZP-R between < and > 60min SE duration
# plot2: across 3 time intervals and separated across economic area
# plot3 (original): age group of study participants and weighted by number of study participants

def fig1B(data):

    total_episodes = data['episodes'].sum()

    freq = data['state'].value_counts()

    sub30 = np.zeros(shape=(len(data),2))
    over30sub60 = np.zeros(shape=(len(data),2))
    sub60 = np.zeros(shape=(len(data),2))
    over60 = np.zeros(shape=(len(data),2))

    for i in range(len(data)):
        
        group = data.state[i]
        
        episodes = data.episodes[i]
        
        weight = episodes/total_episodes*500
        
        resistance = data.resistance[i]*100
        
        age = data.age[i]
        
        phase = data.phase[i]
            
        if phase == '10-30min':
            
            sub30[i,0] = resistance
            
            sub30[i,1] = episodes

            sub60[i,0] = resistance
            
            sub60[i,1] = episodes

        elif phase == '31-60min':
            
            over30sub60[i,0] = resistance
            
            over30sub60[i,1] = episodes

            sub60[i,0] = resistance
            
            sub60[i,1] = episodes

        elif phase == '>60min':
            
            over60[i,0] = resistance
            
            over60[i,1] = episodes

    sub30_list = np.where(sub30[:,1]>0)
    sub30_list[0].tolist()
    sub30_list=sub30_list[0]

    over30sub60_list = np.where(over30sub60[:,1]>0)
    over30sub60_list[0].tolist()
    over30sub60_list=over30sub60_list[0]

    sub60_list = np.where(sub60[:,1]>0)
    sub60_list[0].tolist()
    sub60_list=sub60_list[0]

    over60_list = np.where(over60[:,1]>0)
    over60_list[0].tolist()
    over60_list=over60_list[0]

    sub30_f = np.zeros(shape=(len(sub30_list),3))
    over30sub60_f = np.zeros(shape=(len(over30sub60_list),3))
    sub60_f = np.zeros(shape=(len(sub60_list),3))
    over60_f = np.zeros(shape=(len(over60_list),3))

    for i in range(len(sub30_list)):
        
        index = sub30_list[i]
        
        sub30_f[i,0] = sub30[index,0]
        sub30_f[i,1] = sub30[index,1]
        sub30_f[i,2] = sub30_f[i,0]*sub30_f[i,1]
        
    for i in range(len(over30sub60_list)):
        
        index = over30sub60_list[i]
        
        over30sub60_f[i,0] = over30sub60[index,0]
        over30sub60_f[i,1] = over30sub60[index,1]
        over30sub60_f[i,2] = over30sub60_f[i,0]*over30sub60_f[i,1]

    for i in range(len(sub60_list)):
        
        index = sub60_list[i]
        
        sub60_f[i,0] = sub60[index,0]
        sub60_f[i,1] = sub60[index,1]
        sub60_f[i,2] = sub60_f[i,0]*sub60_f[i,1]    
        
    for i in range(len(over60_list)):
        
        index = over60_list[i]
        
        over60_f[i,0] = over60[index,0]
        over60_f[i,1] = over60[index,1]
        over60_f[i,2] = over60_f[i,0]*over60_f[i,1]    
        
    #calculating mean across phases (%)

    mean_sub30 = np.mean(sub30_f[:,0])

    mean_over30sub60 = np.mean(over30sub60_f[:,0])

    mean_sub60 = np.mean(sub60_f[:,0])

    mean_over60 = np.mean(over60_f[:,0])

    #performaing comparative statistics on <60 and >60min groups (i.e. sub60 vs over60)

    #working out ditribution of resistance values
    shapiro_data1 = stats.shapiro(sub60_f[:,0])
    shapiro_data2 = stats.shapiro(over60_f[:,0])

    #perfomring comparative statistics based on the the distribution of the resistance values
    if shapiro_data1 or shapiro_data2 >0.05:
        p_value = stats.ttest_ind(sub60_f[:,0],over60_f[:,0])
        test = 'unpaired t-test'

    elif shapiro_data1 or shapiro_data2 <0.05:
        p_value = stats.mannwhitneyu(sub60_f[:,0],over60_f[:,0])
        test = 'mann-whitney'   

    #calculating weighted mean across phases (%)

    mean_diff_sub30 = np.sum(sub30_f[:,2],axis=0)/np.sum(sub30_f[:,1],axis=0)

    mean_diff_over30sub60 = np.sum(over30sub60_f[:,2],axis=0)/np.sum(over30sub60_f[:,1],axis=0)

    mean_diff_sub60 = np.sum(sub60_f[:,2],axis=0)/np.sum(sub60_f[:,1],axis=0)

    mean_diff_over60 = np.sum(over60_f[:,2],axis=0)/np.sum(over60_f[:,1],axis=0)

    Fig1B,ax=plt.subplots(figsize=(5,5))

    plt.title('Fig1B')

    x = [.2,.3]

    for i in range(len(sub60_f)):
                    
            weight = 10
                
            marker = 'o'

            resistance = sub60_f[i,0]

            color = 'purple'

            ax.plot(x[0], resistance,markersize=weight, color = color, marker = marker, alpha=.2)
            
    for i in range(len(over60_f)):
                    
            weight = 10
                
            marker = 'o'

            resistance = over60_f[i,0]

            color = 'purple'

            ax.plot(x[1], resistance,markersize=weight, color = color, marker = marker, alpha=.2)
            
    ax.plot(x[0],mean_sub60, markersize=15, color='purple', marker = 'o')
    ax.plot(x[1],mean_over60, markersize=15, color='purple', marker = 'o')

    plt.xlim(.1,.4)

    ax.set_xticks(x)

    labels = ['<60min','>60min']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')        

    axes_limits = ax.get_ylim()

    ax.plot([x[0],x[1]],[axes_limits[1],axes_limits[1]],color='black', lw=1)

    posOne = x[1]-(x[1]-x[0])+(x[1]-x[0])/4

    p = 'p = ' + str(np.round(p_value[1],2))

    font_size = 10

    ax.annotate(p,(posOne,axes_limits[1]+.5),color = 'black',fontsize=font_size)

    plt.close(Fig1B)

    #outputs from plot1:
    # mean_sub30,
    # mean_over30sub60,
    # mean_sub60,
    # mean_over60,
    # p_value,
    # test,

    # Fig1B,

    # mean_diff_sub30,
    # mean_diff_over30sub60,
    # mean_diff_sub60,
    # mean_diff_over60,

    return(mean_sub30,mean_over30sub60,mean_sub60,mean_over60,p_value,test,Fig1B)

#%%
#plot2

def suppfig1B(data, p_value):

    #hic
    sub30_hic = np.zeros(shape=(len(data),2))
    over30sub60_hic = np.zeros(shape=(len(data),2))
    sub60_hic = np.zeros(shape=(len(data),2))
    over60_hic = np.zeros(shape=(len(data),2))

    for i in range(len(data)):
        
        group = data.state[i]
        
        episodes = data.episodes[i]
        
        resistance = data.resistance[i]*100
        
        phase = data.phase[i]
                
        if phase == '10-30min' and group == 'high-income':
            
            sub30_hic[i,0] = resistance
            
            sub30_hic[i,1] = episodes

            sub60_hic[i,0] = resistance
            
            sub60_hic[i,1] = episodes
            
        elif phase == '31-60min' and group == 'high-income':
            
            over30sub60_hic[i,0] = resistance
            
            over30sub60_hic[i,1] = episodes

            sub60_hic[i,0] = resistance
            
            sub60_hic[i,1] = episodes
            
        elif phase == '>60min' and group == 'high-income':
            
            over60_hic[i,0] = resistance
            
            over60_hic[i,1] = episodes

    sub30_hic_list = np.where(sub30_hic[:,1]>0)
    sub30_hic_list[0].tolist()
    sub30_hic_list=sub30_hic_list[0]

    over30sub60_hic_list = np.where(over30sub60_hic[:,1]>0)
    over30sub60_hic_list[0].tolist()
    over30sub60_hic_list=over30sub60_hic_list[0]

    sub60_hic_list = np.where(sub60_hic[:,1]>0)
    sub60_hic_list[0].tolist()
    sub60_hic_list=sub60_hic_list[0]

    over60_hic_list = np.where(over60_hic[:,1]>0)
    over60_hic_list[0].tolist()
    over60_hic_list=over60_hic_list[0]

    sub30_hic_f = np.zeros(shape=(len(sub30_hic_list),3))
    over30sub60_hic_f = np.zeros(shape=(len(over30sub60_hic_list),3))
    sub60_hic_f = np.zeros(shape=(len(sub60_hic_list),3))
    over60_hic_f = np.zeros(shape=(len(over60_hic_list),3))

    for i in range(len(sub30_hic_list)):
        
        index = sub30_hic_list[i]
        
        sub30_hic_f[i,0] = sub30_hic[index,0]
        sub30_hic_f[i,1] = sub30_hic[index,1]
        sub30_hic_f[i,2] = sub30_hic_f[i,0]*sub30_hic_f[i,1]
        
    for i in range(len(over30sub60_hic_list)):
        
        index = over30sub60_hic_list[i]
        
        over30sub60_hic_f[i,0] = over30sub60_hic[index,0]
        over30sub60_hic_f[i,1] = over30sub60_hic[index,1]
        over30sub60_hic_f[i,2] = over30sub60_hic_f[i,0]*over30sub60_hic_f[i,1]

    for i in range(len(sub60_hic_list)):
        
        index = sub60_hic_list[i]
        
        sub60_hic_f[i,0] = sub60_hic[index,0]
        sub60_hic_f[i,1] = sub60_hic[index,1]
        sub60_hic_f[i,2] = sub60_hic_f[i,0]*sub60_hic_f[i,1]    
        
    for i in range(len(over60_hic_list)):
        
        index = over60_hic_list[i]
        
        over60_hic_f[i,0] = over60_hic[index,0]
        over60_hic_f[i,1] = over60_hic[index,1]
        over60_hic_f[i,2] = over60_hic_f[i,0]*over60_hic_f[i,1]    

    #calculating mean across phases (%)

    mean_sub30_hic = np.mean(sub30_hic_f[:,0])

    mean_over30sub60_hic = np.mean(over30sub60_hic_f[:,0])

    mean_sub60_hic = np.mean(sub60_hic_f[:,0])

    mean_over60_hic = np.mean(over60_hic_f[:,0])

    #performaing comparative statistics on <60 and >60min groups (i.e. sub60 vs over60)

    #working out ditribution of resistance values
    shapiro_data1 = stats.shapiro(sub60_hic_f[:,0])
    shapiro_data2 = stats.shapiro(over60_hic_f[:,0])

    #perfomring comparative statistics based on the the distribution of the resistance values
    if shapiro_data1 or shapiro_data2 >0.05:
        p_value_hic = stats.ttest_ind(sub60_hic_f[:,2],over60_hic_f[:,0])
        test_hic = 'unpaired t-test'

    elif shapiro_data1 or shapiro_data2 <0.05:
        p_value_hic = stats.mannwhitneyu(sub60_hic_f[:,0],over60_hic_f[:,0])
        test_hic = 'mann-whitney'   

    #calculating weighted mean across phases (%)

    mean_diff_sub30_hic = np.sum(sub30_hic_f[:,2],axis=0)/np.sum(sub30_hic_f[:,1],axis=0)

    mean_diff_over30sub60_hic = np.sum(over30sub60_hic_f[:,2],axis=0)/np.sum(over30sub60_hic_f[:,1],axis=0)

    mean_diff_sub60_hic = np.sum(sub60_hic_f[:,2],axis=0)/np.sum(sub60_hic_f[:,1],axis=0)

    mean_diff_over60_hic = np.sum(over60_hic_f[:,2],axis=0)/np.sum(over60_hic_f[:,1],axis=0)

    #lmic
    sub30_lmic = np.zeros(shape=(len(data),2))
    over30sub60_lmic = np.zeros(shape=(len(data),2))
    sub60_lmic = np.zeros(shape=(len(data),2))
    over60_lmic = np.zeros(shape=(len(data),2))

    for i in range(len(data)):
        
        group = data.state[i]
        
        episodes = data.episodes[i]
        
        resistance = data.resistance[i]*100
        
        phase = data.phase[i]
                
        if phase == '10-30min' and group == 'low-middle-income':
            
            sub30_lmic[i,0] = resistance
            
            sub30_lmic[i,1] = episodes

            sub60_lmic[i,0] = resistance
            
            sub60_lmic[i,1] = episodes
            
        elif phase == '31-60min' and group == 'low-middle-income':
            
            over30sub60_lmic[i,0] = resistance
            
            over30sub60_lmic[i,1] = episodes

            sub60_lmic[i,0] = resistance
            
            sub60_lmic[i,1] = episodes
            
        elif phase == '>60min' and group == 'low-middle-income':
            
            over60_lmic[i,0] = resistance
            
            over60_lmic[i,1] = episodes

    sub30_lmic_list = np.where(sub30_lmic[:,1]>0)
    sub30_lmic_list[0].tolist()
    sub30_lmic_list=sub30_lmic_list[0]

    over30sub60_lmic_list = np.where(over30sub60_lmic[:,1]>0)
    over30sub60_lmic_list[0].tolist()
    over30sub60_lmic_list=over30sub60_lmic_list[0]

    sub60_lmic_list = np.where(sub60_lmic[:,1]>0)
    sub60_lmic_list[0].tolist()
    sub60_lmic_list=sub60_lmic_list[0]

    over60_lmic_list = np.where(over60_lmic[:,1]>0)
    over60_lmic_list[0].tolist()
    over60_lmic_list=over60_lmic_list[0]

    sub30_lmic_f = np.zeros(shape=(len(sub30_lmic_list),3))
    over30sub60_lmic_f = np.zeros(shape=(len(over30sub60_lmic_list),3))
    sub60_lmic_f = np.zeros(shape=(len(sub60_lmic_list),3))
    over60_lmic_f = np.zeros(shape=(len(over60_lmic_list),3))

    for i in range(len(sub30_lmic_list)):
        
        index = sub30_lmic_list[i]
        
        sub30_lmic_f[i,0] = sub30_lmic[index,0]
        sub30_lmic_f[i,1] = sub30_lmic[index,1]
        sub30_lmic_f[i,2] = sub30_lmic_f[i,0]*sub30_hic_f[i,1]
        
    for i in range(len(over30sub60_lmic_list)):
        
        index = over30sub60_lmic_list[i]
        
        over30sub60_lmic_f[i,0] = over30sub60_lmic[index,0]
        over30sub60_lmic_f[i,1] = over30sub60_lmic[index,1]
        over30sub60_lmic_f[i,2] = over30sub60_lmic_f[i,0]*over30sub60_lmic_f[i,1]

    for i in range(len(sub60_lmic_list)):
        
        index = sub60_lmic_list[i]
        
        sub60_lmic_f[i,0] = sub60_lmic[index,0]
        sub60_lmic_f[i,1] = sub60_lmic[index,1]
        sub60_lmic_f[i,2] = sub60_lmic_f[i,0]*sub60_lmic_f[i,1]    
        
    for i in range(len(over60_lmic_list)):
        
        index = over60_lmic_list[i]
        
        over60_lmic_f[i,0] = over60_lmic[index,0]
        over60_lmic_f[i,1] = over60_lmic[index,1]
        over60_lmic_f[i,2] = over60_lmic_f[i,0]*over60_lmic_f[i,1]    

    #calculating mean across phases (%)

    mean_sub30_lmic = np.mean(sub30_lmic_f[:,0])

    mean_over30sub60_lmic = np.mean(over30sub60_lmic_f[:,0])

    mean_sub60_lmic = np.mean(sub60_lmic_f[:,0])

    mean_over60_lmic = np.mean(over60_lmic_f[:,0])

    #performaing comparative statistics on <60 and >60min groups (i.e. sub60 vs over60)

    #working out ditribution of resistance values
    shapiro_data1 = stats.shapiro(sub60_lmic_f[:,0])
    shapiro_data2 = stats.shapiro(over60_lmic_f[:,0])

    #perfomring comparative statistics based on the the distribution of the resistance values
    if shapiro_data1 or shapiro_data2 >0.05:
        p_value_lmic = stats.ttest_ind(sub60_lmic_f[:,0],over60_lmic_f[:,0])
        test_lmic = 'unpaired t-test'

    elif shapiro_data1 or shapiro_data2 <0.05:
        p_value_lmic = stats.mannwhitneyu(sub60_lmic_f[:,0],over60_lmic_f[:,0])
        test_lmic = 'mann-whitney'   

    #calculating weighted mean across phases (%)

    mean_diff_sub30_lmic = np.sum(sub30_lmic_f[:,2],axis=0)/np.sum(sub30_lmic_f[:,1],axis=0)

    mean_diff_over30sub60_lmic = np.sum(over30sub60_lmic_f[:,2],axis=0)/np.sum(over30sub60_lmic_f[:,1],axis=0)

    mean_diff_sub60_lmic = np.sum(sub60_lmic_f[:,2],axis=0)/np.sum(sub60_lmic_f[:,1],axis=0)

    mean_diff_over60_lmic = np.sum(over60_lmic_f[:,2],axis=0)/np.sum(over60_lmic_f[:,1],axis=0)

    #plotting figure

    SuppFig1B,ax=plt.subplots(figsize=(5,5))

    plt.title('SuppFig1B')

    x = [.2,.3]

    for i in range(len(sub60_hic_f)):
                    
            weight = 10
                
            marker = 'o'

            resistance = sub60_hic_f[i,0]

            color = 'blue'

            ax.plot(x[0]-.01, resistance,markersize=weight, color = color, marker = marker, alpha=.2)

    for i in range(len(over60_hic_f)):
                    
            weight = 10
                
            marker = 'o'

            resistance = sub60_hic_f[i,0]

            color = 'blue'

            ax.plot(x[1]-.01, resistance,markersize=weight, color = color, marker = marker, alpha=.2)        
            
    for i in range(len(sub60_lmic_f)):
                    
            weight = 10
                
            marker = 'o'

            resistance = sub60_lmic_f[i,0]

            color = 'red'

            ax.plot(x[0]+.01, resistance,markersize=weight, color = color, marker = marker, alpha=.2)

    for i in range(len(over60_lmic_f)):
                    
            weight = 10
                
            marker = 'o'

            resistance = over60_lmic_f[i,0]

            color = 'red'

            ax.plot(x[1]+.01, resistance,markersize=weight, color = color, marker = marker, alpha=.2)  
            
    ax.plot(x[0]-.01,mean_sub60_hic, markersize=15, color='blue', marker = 'o')
    ax.plot(x[1]-.01,mean_over60_hic, markersize=15, color='blue', marker = 'o')

    ax.plot(x[0]+.01,mean_sub60_lmic, markersize=15, color='red', marker = 'o')
    ax.plot(x[1]+.01,mean_over60_lmic, markersize=15, color='red', marker = 'o')

    plt.xlim(.1,.4)

    ax.set_xticks(x)

    labels = ['<60min','>60min']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')        

    axes_limits = ax.get_ylim()

    ax.plot([x[0],x[1]],[axes_limits[1],axes_limits[1]],color='black', lw=1)

    posOne = x[1]-(x[1]-x[0])+(x[1]-x[0])/4

    p = 'p = ' + str(np.round(p_value[1],2))

    font_size = 10

    ax.annotate(p,(posOne,axes_limits[1]+.5),color = 'black',fontsize=font_size)

    plt.close(SuppFig1B)

    data_hic = {
                            'Mean 10-30min HIC' : mean_sub30_hic,
                            'Mean 31-60min HIC' : mean_over30sub60_hic, 
                            'Mean <60min HIC'       : mean_sub60_hic,
                            'Mean >60min HIC'       : mean_over60_hic,
                            'p-value HIC'       : p_value_hic,
                            'Test HIC'              : test_hic
                            }

    data_lmic = {
                            'Mean 10-30min LMIC' : mean_sub30_lmic,
                            'Mean 31-60min LMIC' : mean_over30sub60_lmic, 
                            'Mean <60min LMIC'        : mean_sub60_lmic,
                            'Mean >60min LMIC'        : mean_over60_lmic,
                            'p-value LMIC'       : p_value_lmic,
                            'Test LMIC'               : test_lmic
                            }

    return(data_hic, data_lmic, SuppFig1B)

# #%%

# #plot 3

# lmic_sub60 = len(sub60_lmic_f[:,0])/(len(sub60_lmic_f[:,0])+len(over60_lmic_f[:,0]))*100
# lmic_over60 = len(over60_lmic_f[:,0])/(len(sub60_lmic_f[:,0])+len(over60_lmic_f[:,0]))*100

# hic_sub60 = len(sub60_hic_f[:,0])/(len(sub60_hic_f[:,0])+len(over60_hic_f[:,0]))*100
# hic_over60 = len(over60_hic_f[:,0])/(len(sub60_hic_f[:,0])+len(over60_hic_f[:,0]))*100

# table = np.array([[lmic_sub60, lmic_over60], [hic_sub60, hic_over60]])

# oddsr, p_fish = stats.fisher_exact(table, alternative='two-sided')

# if p_fish <0.0001: 

#             p_fish = str('<0.0001')

# else:
#     p_fish = str(np.round(p_fish,2))
    
# SuppFig1C,ax=plt.subplots(figsize=(5,5))

# plt.title('SuppFig1C')

# ax.bar([.2,.3], [hic_sub60,lmic_sub60], color=['blue','red'], alpha = 1, width = .05)

# ax.bar([.2,.3], [hic_over60,lmic_over60], bottom = [hic_sub60,lmic_sub60],color=['blue','red'], alpha = .90, width = .05, hatch = '/')

# ax.set_ylabel('Percentage (%)')

# x = [.2,.3]

# labels = ['<60min','>60min']

# ax.set_xticks(x)

# ax.set_xticklabels(labels)  

# plt.xlim(.1,.4)

# axes_limits = ax.get_ylim()

# ax.plot([x[0],x[1]],[axes_limits[1],axes_limits[1]],color='black', lw=1)

# posOne = x[1]-(x[1]-x[0])+(x[1]-x[0])/4

# font_size = 10

# ax.annotate(p_fish,(posOne,axes_limits[1]+.5),color = 'black',fontsize=font_size)

# plt.show()

# #%%    


# SuppFig1D,ax=plt.subplots(figsize=(5,5))

# plt.title('SuppFig1D')

# x = [.2,.3,.4]

# ax.set_xticklabels(labels)

# ax.set_ylabel('BZP-R (%)')

# #plotting original figure with all detail (i.e. stratified across duration of SE, age of participants, number of participants and economic groups)
    
# sub30 = np.zeros(shape=(len(data),2))
# over30sub60 = np.zeros(shape=(len(data),2))
# over60 = np.zeros(shape=(len(data),2))

# for i in range(len(data)):
    
#     group = data.state[i]
    
#     episodes = data.episodes[i]
    
#     weight = episodes/total_episodes*500
    
#     resistance = data.resistance[i]*100
    
#     age = data.age[i]
    
#     phase = data.phase[i]
    
#     marker = 'o'
    
#     if age == 'paediatric':
        
#         color = 'magenta'

#     elif age == 'adult':
        
#         color = 'orange'

#     elif age == 'both':
        
#         color = 'black'           

#     if phase == '10-30min' and group == 'high-income':
        
#         sub30[i,0] = resistance
        
#         sub30[i,1] = episodes
        
#         ax.plot(x[0]-.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)
#         ax.plot(x[0]-.015, resistance,markersize=weight, color = 'blue', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)
    
#     elif phase == '10-30min' and group == 'low-middle-income':
        
#         sub30[i,0] = resistance
        
#         sub30[i,1] = episodes
        
#         ax.plot(x[0]+.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)
#         ax.plot(x[0]+.015, resistance,markersize=weight, color = 'red', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)
    
#     elif phase == '31-60min' and group == 'high-income':
        
#         over30sub60[i,0] = resistance
        
#         over30sub60[i,1] = episodes
        
#         ax.plot(x[1]-.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2,alpha=.2)        
#         ax.plot(x[1]-.015, resistance,markersize=weight, color = 'blue', marker = marker, markeredgecolor = color, markeredgewidth=2,alpha=.2)        

#     elif phase == '31-60min' and group == 'low-middle-income':
        
#         over30sub60[i,0] = resistance
        
#         over30sub60[i,1] = episodes
        
#         ax.plot(x[1]+.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2,alpha=.2)               
#         ax.plot(x[1]+.015, resistance,markersize=weight, color = 'red', marker = marker, markeredgecolor = color, markeredgewidth=2,alpha=.2)               
               
#     elif phase == '>60min' and group == 'high-income':
        
#         over60[i,0] = resistance
        
#         over60[i,1] = episodes
        
#         ax.plot(x[2]-.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)        
#         ax.plot(x[2]-.015, resistance,markersize=weight, color = 'blue', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)        

#     elif phase == '>60min' and group == 'low-middle-income':
        
#         over60[i,0] = resistance
        
#         over60[i,1] = episodes
        
#         ax.plot(x[2]+.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)        
#         ax.plot(x[2]+.015, resistance,markersize=weight, color = 'red', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)        
        

# ax.plot(x[0],mean_diff_sub30, markersize=15, color='purple', marker = 'o')
# ax.plot(x[1],mean_diff_over30sub60, markersize=15, color='purple', marker = 'o')
# ax.plot(x[2],mean_diff_over60, markersize=15, color='purple', marker = 'o')

# plt.xlim(.1,.5)

# ax.set_xticks(x)

# labels = ['10-30min','31-60min','>60min']

# ax.set_xticklabels(labels)

# ax.set_ylabel('BZP-R (%)')

# ax.plot(.125,80,markersize=10,marker='o',color='white',markeredgecolor = 'orange')
# plt.text(.140, 78, 'Adult only', fontsize=12)

# ax.plot(.125,75,markersize=10,marker='o',color='white',markeredgecolor = 'magenta')
# plt.text(.140, 73, 'Paediatric only', fontsize=12)

# ax.plot(.125,70,markersize=10,marker='o',color='white',markeredgecolor = 'black')
# plt.text(.140, 68, 'Mixed', fontsize=12)

# ax.plot(.125,65,markersize=10,marker='o',color='purple')

# plt.text(.140, 63, 'Mean diff.', fontsize=12)

# ax.plot(.125,60,markersize=10,marker='_',color='blue')
# plt.text(.140, 58, 'HIC', fontsize=12)

# ax.plot(.125,55,markersize=10,marker='_',color='red')
# plt.text(.140, 53, 'LMIC', fontsize=12)


