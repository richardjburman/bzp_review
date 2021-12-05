#%%
#functions used in Fig1 code
#created RJ Burman 28 Nov 2021

#%%
#importing libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
import seaborn as sns
from scipy import stats
from tabulate import tabulate
from statsmodels.stats.weightstats import DescrStatsW

#%%
def fig1A(data):

    total_episodes = data['episodes'].sum()

    hic = np.zeros(shape=(len(data),2))
    lmic = np.zeros(shape=(len(data),2))
    total = np.zeros(shape=(len(data),3))

    for i in range(len(data)):
        
        group = data.state[i]
        
        episodes = data.episodes[i]
               
        resistance = data.resistance[i]
        
        total[i,0] = resistance

        total[i,1] = episodes
        
        total[i,2] = episodes*resistance
            
        if group == 'HIC':
            
            hic[i,0] = resistance
            
            hic[i,1] = episodes

        elif group == 'LMIC':
            
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
    
    mean_hic = np.mean(hic_final[:,0])
    sem_hic = stats.sem(hic_final[:,0])

    mean_lmic = np.mean(lmic_final[:,0])
    sem_lmic = stats.sem(lmic_final[:,0])

    mean_total = np.mean(total[:,0])
    sem_total = stats.sem(total[:,0])

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

    mean_diff_hic = np.sum(lmic_final[:,2],axis=0)/np.sum(lmic_final[:,1],axis=0)
    
    mean_diff_lmic = np.sum(lmic_final[:,2],axis=0)/np.sum(lmic_final[:,1],axis=0)

    mean_diff_total = np.sum(total[:,2],axis=0)/np.sum(total[:,1],axis=0)

    hic_data = hic_final[:,0]
    hic_weights = hic_final[:,1]

    weighted_stats_hic = DescrStatsW(hic_data, hic_weights, ddof=0)

    lmic_data = lmic_final[:,0]
    lmic_weights = lmic_final[:,1]

    weighted_stats_lmic = DescrStatsW(lmic_data, lmic_weights, ddof=0)

    total_data = total[:,0]
    total_weights = total[:,1]

    weighted_stats_total = DescrStatsW(total_data, total_weights, ddof=0)

    nonweighted_stats = {
                                'Mean HIC' : mean_hic,
                                'SEM HIC': sem_hic,
                                'Mean LMIC' : mean_lmic,
                                'SEM LMIC' : sem_lmic,
                                'Mean Total' : mean_total,
                                'SEM Total' : sem_total,
                                'p-value' : p_value,
                                'test' : test,
                                
                            }

    weighted_stats = {
                        'Weighted Mean HIC' : weighted_stats_hic.mean,
                        'Weighted SEM HIC': weighted_stats_hic.std_mean,
                        'Weighted Mean LMIC' : weighted_stats_lmic.mean,
                        'Weighted SEM LMIC' : weighted_stats_lmic.std_mean,
                        'Weighted Mean Total' : weighted_stats_total.mean,
                        'Weighted SEM Total' : weighted_stats_total.std_mean,
                    }
   
    #plotting new figure which collapses data to separate only between economic groups

    Fig1A,ax=plt.subplots(figsize=(5,5))

    plt.title('Fig1A')

    x = [.2,.3]

    total_episodes = data['episodes'].sum()

    freq = data['state'].value_counts()

    for i in range(len(data)):
        
        group = data.state[i]
                
        resistance = data.resistance[i]
               
        if group == 'HIC':
            
            ax.plot(x[0], resistance,markersize=10, color='blue', marker = 'o',alpha=.2)

        elif group == 'LMIC':
            
            ax.plot(x[1], resistance,markersize=10, color='red', marker = 'o',alpha=.2)    
            
    plt.xlim(.1,.4)

    ax.set_xticks(x)

    labels = ['HIC','LMIC']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')

    ax.plot([x[0],x[0]],[mean_hic-sem_hic,mean_hic+sem_hic],color='blue', lw=3)
    ax.plot([x[1],x[1]],[mean_lmic-sem_lmic,mean_lmic+sem_lmic],color='red', lw=3)
    ax.plot([.25,.25],[mean_total-sem_total,mean_total+sem_total],color='purple', lw=3)

    ax.plot(x[0],mean_hic, markersize=15, color='white',markeredgecolor = 'blue', marker = 'o')
    ax.plot(x[1],mean_lmic, markersize=15, color='white',markeredgecolor = 'red', marker = 'o')
    ax.plot(.25,mean_total, markersize=15, color='white',markeredgecolor = 'purple', marker = 'o')

    ax.plot(.115,88,markersize=10, color='white',markeredgecolor = 'purple', marker = 'o')
    plt.text(.130, 86, 'Mean total', fontsize=12)

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
    
        resistance = data.resistance[i]
    
        age = data.age[i]
    
        if group == 'HIC' and age == 'adult':
        
            ax.plot(x[0]-.015, resistance,markersize=weight, color='blue', marker = 'o',alpha=.2)
   
        elif group == 'HIC' and age == 'paediatric':
        
            ax.plot(x[0]+.015, resistance,markersize=weight, color='magenta', marker = 'o',alpha=.2)
        
        elif group == 'HIC' and age == 'both':
        
            ax.plot(x[0], resistance,markersize=weight, color='black', marker = 'o',alpha=.2)        

        elif group == 'LMIC' and age == 'adult':
        
            ax.plot(x[1]-.015, resistance,markersize=weight, color='blue', marker = 'o',alpha=.2)

        elif group == 'LMIC' and age == 'paediatric':
        
            ax.plot(x[1]+.015, resistance,markersize=weight, color='magenta', marker = 'o',alpha=.2)       
        
        elif group == 'LMIC' and age == 'both':
        
            ax.plot(x[1], resistance,markersize=weight, color='black', marker = 'o',alpha=.2)        
        
    plt.xlim(.1,.4)

    ax.set_xticks(x)

    labels = ['HIC','LMIC']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')

    ax.plot(x[0],weighted_stats_hic.mean, markersize=15, color='white', markeredgecolor = 'blue', marker = 'o')
    ax.plot(x[1],weighted_stats_lmic.mean, markersize=15, color='white', markeredgecolor = 'red', marker = 'o')
    ax.plot(.25,weighted_stats_total.mean, markersize=15, color='white', markeredgecolor = 'purple', marker = 'o')

    ax.plot([x[0],x[0]],[weighted_stats_hic.mean-weighted_stats_hic.std_mean,weighted_stats_hic.mean+weighted_stats_hic.std_mean],color='blue', lw=3)
    ax.plot([x[1],x[1]],[weighted_stats_lmic.mean-weighted_stats_lmic.std_mean,weighted_stats_lmic.mean+weighted_stats_lmic.std_mean],color='red', lw=3)
    ax.plot([.25,.25],[weighted_stats_total.mean-weighted_stats_total.std_mean,weighted_stats_total.mean+weighted_stats_total.std_mean],color='purple', lw=3)

    ax.plot(.115,88,markersize=10,marker='o',color='blue',alpha=.2)
    plt.text(.130, 86, 'Adult only', fontsize=12)

    ax.plot(.115,83,markersize=10,marker='o',color='black',alpha=.2)
    plt.text(.130, 81, 'Mixed', fontsize=12)

    ax.plot(.115,78,markersize=10,marker='o',color='magenta',alpha=.2)
    plt.text(.130, 76, 'Paediatric only', fontsize=12)

    ax.plot(.115,73,markersize=10,marker='o',color='white', markeredgecolor = 'purple')
    plt.text(.130, 71, 'Weighted mean', fontsize=12)

    plt.close(SuppFig1A)

    return(Fig1A, SuppFig1A, nonweighted_stats, weighted_stats)

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
        
        resistance = data.resistance[i]
        
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
    sem_sub30 = stats.sem(sub30_f[:,0])

    mean_over30sub60 = np.mean(over30sub60_f[:,0])
    sem_over30sub60 = stats.sem(over30sub60_f[:,0])

    mean_sub60 = np.mean(sub60_f[:,0])
    sem_sub60 = stats.sem(sub60_f[:,0])

    mean_over60 = np.mean(over60_f[:,0])
    sem_over60 = stats.sem(over60_f[:,0])

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

    nonweighted_stats_phases = {

                                    'Mean 10-30min' :  mean_sub30,
                                    'SEM 10-30min': sem_sub30,
                                    'Mean 31-60min' : mean_over30sub60,
                                    'SEM LMIC' : sem_over30sub60,
                                    'Mean <60min' : mean_sub60,
                                    'SEM <60min' : sem_sub60,
                                    'Mean >60min' : mean_over60,
                                    'SEM >60min' : sem_over60,
                                    'p-value' : p_value,
                                    'test' : test
                        
                               }

    sub30_data = sub30_f[:,0]
    sub30_weights = sub30_f[:,1]

    weighted_stats_sub30 = DescrStatsW(sub30_data, sub30_weights, ddof=0)

    over30sub60_data = over30sub60_f[:,0]
    over30sub60_weights = over30sub60_f[:,1]

    weighted_stats_over30sub60 = DescrStatsW(over30sub60_data, over30sub60_weights, ddof=0)

    sub60_data = sub60_f[:,0]
    sub60_weights = sub60_f[:,1]

    weighted_stats_sub60 = DescrStatsW(sub60_data, sub60_weights, ddof=0)

    over60_data = over60_f[:,0]
    over60_weights = over60_f[:,1]

    weighted_stats_over60 = DescrStatsW(over60_data, over60_weights, ddof=0)

    weighted_stats_phases = {

                    'Weighted Mean 10-30min' : weighted_stats_sub30.mean,
                    'Weighted SEM 10-30min': weighted_stats_sub30.std_mean,
                    'Weighted Mean 31-60min' : weighted_stats_over30sub60.mean,
                    'Weighted SEM 31-60min' : weighted_stats_over30sub60.std_mean,
                    'Weighted Mean <60min' : weighted_stats_sub60.mean,
                    'Weighted SEM <60min' : weighted_stats_sub60.std_mean,
                    'Weighted Mean >60min' : weighted_stats_over60.mean,
                    'Weighted SEM >60min' : weighted_stats_over60.std_mean,                  

                }

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

    ax.plot([x[0],x[0]],[mean_sub60-sem_sub60,mean_sub60+sem_sub60],color='purple', lw=3)
    ax.plot([x[1],x[1]],[mean_over60-sem_over60,mean_over60+sem_over60],color='purple', lw=3)

    ax.plot(x[0],mean_sub60, markersize=15, color='white', markeredgecolor = 'purple', marker = 'o')
    ax.plot(x[1],mean_over60, markersize=15, color='white', markeredgecolor = 'purple', marker = 'o')

    plt.xlim(.1,.4)

    ax.set_xticks(x)

    labels = ['<60min','>60min']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')        

    axes_limits = ax.get_ylim()

    ax.plot([x[0],x[1]],[axes_limits[1],axes_limits[1]],color='black', lw=1)

    posOne = x[1]-(x[1]-x[0])+(x[1]-x[0])/4

    p = 'p = ' + str(np.round(p_value[1],4))

    font_size = 10

    ax.annotate(p,(posOne,axes_limits[1]+.5),color = 'black',fontsize=font_size)

    plt.close(Fig1B)

    return(Fig1B, nonweighted_stats_phases, weighted_stats_phases)

#%%
#function to generate supplementary figures to complement Figure 1B

def suppfigs(data, p_value, weighted_stats_phases):

    mean_diff_sub30 = weighted_stats_phases['Weighted Mean 10-30min']
    sem_diff_sub30 = weighted_stats_phases['Weighted SEM 10-30min']

    mean_diff_over30sub60 = weighted_stats_phases ['Weighted Mean 31-60min']
    sem_diff_over30sub60 = weighted_stats_phases['Weighted SEM 31-60min']

    mean_diff_sub60 = weighted_stats_phases ['Weighted Mean <60min']
    sem_diff_sub60 = weighted_stats_phases['Weighted SEM <60min']

    mean_diff_over60 = weighted_stats_phases ['Weighted Mean >60min']
    sem_diff_over60 = weighted_stats_phases['Weighted SEM >60min']

    #hic
    sub30_hic = np.zeros(shape=(len(data),2))
    over30sub60_hic = np.zeros(shape=(len(data),2))
    sub60_hic = np.zeros(shape=(len(data),2))
    over60_hic = np.zeros(shape=(len(data),2))

    for i in range(len(data)):
        
        group = data.state[i]
        
        episodes = data.episodes[i]
        
        resistance = data.resistance[i]
        
        phase = data.phase[i]
                
        if phase == '10-30min' and group == 'HIC':
            
            sub30_hic[i,0] = resistance
            
            sub30_hic[i,1] = episodes

            sub60_hic[i,0] = resistance
            
            sub60_hic[i,1] = episodes
            
        elif phase == '31-60min' and group == 'HIC':
            
            over30sub60_hic[i,0] = resistance
            
            over30sub60_hic[i,1] = episodes

            sub60_hic[i,0] = resistance
            
            sub60_hic[i,1] = episodes
            
        elif phase == '>60min' and group == 'HIC':
            
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
    sem_sub30_hic = stats.sem(sub30_hic_f[:,0])

    mean_over30sub60_hic = np.mean(over30sub60_hic_f[:,0])
    sem_over30sub60_hic = stats.sem(over30sub60_hic_f[:,0])

    mean_sub60_hic = np.mean(sub60_hic_f[:,0])
    sem_sub60_hic = stats.sem(sub60_hic_f[:,0])

    mean_over60_hic = np.mean(over60_hic_f[:,0])
    sem_over60_hic = stats.sem(over60_hic_f[:,0])

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

    sub30_hic_data = sub30_hic_f[:,0]
    sub30_hic_weights = sub30_hic_f[:,1]

    weighted_stats_hic_sub30 = DescrStatsW(sub30_hic_data, sub30_hic_weights, ddof=0)

    over30sub60_hic_data = over30sub60_hic_f[:,0]
    over30sub60_hic_weights = over30sub60_hic_f[:,1]

    weighted_stats_hic_over30sub60 = DescrStatsW(over30sub60_hic_data, over30sub60_hic_weights, ddof=0)

    sub60_hic_data = sub60_hic_f[:,0]
    sub60_hic_weights = sub60_hic_f[:,1]

    weighted_stats_hic_sub60 = DescrStatsW(sub60_hic_data, sub60_hic_weights, ddof=0)

    over60_hic_data = over60_hic_f[:,0]
    over60_hic_weights = over60_hic_f[:,1]

    weighted_stats_hic_over60 = DescrStatsW(over60_hic_data, over60_hic_weights, ddof=0)

    #lmic
    sub30_lmic = np.zeros(shape=(len(data),2))
    over30sub60_lmic = np.zeros(shape=(len(data),2))
    sub60_lmic = np.zeros(shape=(len(data),2))
    over60_lmic = np.zeros(shape=(len(data),2))

    for i in range(len(data)):
        
        group = data.state[i]
        
        episodes = data.episodes[i]
        
        resistance = data.resistance[i]
        
        phase = data.phase[i]
                
        if phase == '10-30min' and group == 'LMIC':
            
            sub30_lmic[i,0] = resistance
            
            sub30_lmic[i,1] = episodes

            sub60_lmic[i,0] = resistance
            
            sub60_lmic[i,1] = episodes
            
        elif phase == '31-60min' and group == 'LMIC':
            
            over30sub60_lmic[i,0] = resistance
            
            over30sub60_lmic[i,1] = episodes

            sub60_lmic[i,0] = resistance
            
            sub60_lmic[i,1] = episodes
            
        elif phase == '>60min' and group == 'LMIC':
            
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
    sem_sub30_lmic = stats.sem(sub30_lmic_f[:,0])

    mean_over30sub60_lmic = np.mean(over30sub60_lmic_f[:,0])
    sem_over30sub60_lmic = stats.sem(over30sub60_lmic_f[:,0])

    mean_sub60_lmic = np.mean(sub60_lmic_f[:,0])
    sem_sub60_lmic = stats.sem(sub60_lmic_f[:,0])

    mean_over60_lmic = np.mean(over60_lmic_f[:,0])
    sem_over60_lmic = stats.sem(over60_lmic_f[:,0])

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

    sub30_lmic_data = sub30_lmic_f[:,0]
    sub30_lmic_weights = sub30_lmic_f[:,1]

    weighted_stats_lmic_sub30 = DescrStatsW(sub30_lmic_data, sub30_lmic_weights, ddof=0)

    over30sub60_lmic_data = over30sub60_lmic_f[:,0]
    over30sub60_lmic_weights = over30sub60_lmic_f[:,1]

    weighted_stats_lmic_over30sub60 = DescrStatsW(over30sub60_lmic_data, over30sub60_lmic_weights, ddof=0)

    sub60_lmic_data = sub60_lmic_f[:,0]
    sub60_lmic_weights = sub60_lmic_f[:,1]

    weighted_stats_lmic_sub60 = DescrStatsW(sub60_lmic_data, sub60_lmic_weights, ddof=0)

    over60_lmic_data = over60_lmic_f[:,0]
    over60_lmic_weights = over60_lmic_f[:,1]

    weighted_stats_lmic_over60 = DescrStatsW(over60_lmic_data, over60_lmic_weights, ddof=0)

    nonweighted_stats_phases_eco = {

                                    'HIC Mean 10-30min' :  mean_sub30_hic,
                                    'HIC SEM 10-30min': sem_sub30_hic,
                                    'HIC Mean 31-60min' : mean_over30sub60_hic,
                                    'HIC SEM 31-60min' : sem_over30sub60_hic,
                                    'HIC Mean <60min' : mean_sub60_hic,
                                    'HIC SEM <60min' : sem_sub60_hic,
                                    'HIC Mean >60min' : mean_over60_hic,
                                    'HIC SEM >60min' : sem_over60_hic,
                                    'p-value HIC' :  p_value_hic,
                                    'test HIC' :  test_hic,

                                    'LMIC Mean 10-30min' :  mean_sub30_lmic,
                                    'LMIC SEM 10-30min': sem_sub30_lmic,
                                    'LMIC Mean 31-60min' : mean_over30sub60_lmic,
                                    'LMIC SEM 31-60min' : sem_over30sub60_lmic,
                                    'LMIC Mean <60min' : mean_sub60_lmic,
                                    'LMIC SEM <60min' : sem_sub60_lmic,
                                    'LMIC Mean >60min' : mean_over60_lmic,
                                    'LMIC SEM >60min' : sem_over60_lmic,
                                    'p-value LMIC' :  p_value_lmic,
                                    'test LMIC' :  test_lmic     
                        
                                    }

    weighted_stats_phases_eco = {

                    'HIC Weighted Mean 10-30min' : weighted_stats_hic_sub30.mean,
                    'HIC Weighted SEM 10-30min': weighted_stats_hic_sub30.std_mean,
                    'HIC Weighted Mean 31-60min' : weighted_stats_hic_over30sub60.mean,
                    'HIC Weighted SEM 31-60min' : weighted_stats_hic_over30sub60.std_mean,
                    'HIC Weighted Mean <60min' : weighted_stats_hic_sub60.mean,
                    'HIC Weighted SEM <60min' : weighted_stats_hic_sub60.std_mean,
                    'HIC Weighted Mean >60min' : weighted_stats_hic_over60.mean,
                    'HIC Weighted SEM >60min' : weighted_stats_hic_over60.std_mean,


                    'LMIC Weighted Mean 10-30min' : weighted_stats_lmic_sub30.mean,
                    'LMIC Weighted SEM 10-30min': weighted_stats_lmic_sub30.std_mean,
                    'LMIC Weighted Mean 31-60min' : weighted_stats_lmic_over30sub60.mean,
                    'LMIC Weighted SEM 31-60min' : weighted_stats_lmic_over30sub60.std_mean,
                    'LMIC Weighted Mean <60min' : weighted_stats_lmic_sub60.mean,
                    'LMIC Weighted SEM <60min' : weighted_stats_lmic_sub60.std_mean,
                    'LMIC Weighted Mean >60min' : weighted_stats_lmic_over60.mean,
                    'LMIC Weighted SEM >60min' : weighted_stats_lmic_over60.std_mean,
             
                                 }  

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

    ax.plot([x[0]-.01,x[0]-.01],[mean_sub60_hic-sem_sub60_hic,mean_sub60_hic+sem_sub60_hic],color='blue', lw=3)
    ax.plot([x[1]-.01,x[1]-.01],[mean_over60_hic-sem_over60_hic,mean_over60_hic+sem_over60_hic],color='blue', lw=3)

    ax.plot([x[0]+.01,x[0]+.01],[mean_sub60_lmic-sem_sub60_lmic,mean_sub60_lmic+sem_sub60_lmic],color='red', lw=3)
    ax.plot([x[1]+.01,x[1]+.01],[mean_over60_lmic-sem_over60_lmic,mean_over60_lmic+sem_over60_lmic],color='red', lw=3)

    ax.plot(x[0]-.01,mean_sub60_hic, markersize=15, color='white', markeredgecolor = 'blue', marker = 'o')
    ax.plot(x[1]-.01,mean_over60_hic, markersize=15, color='white', markeredgecolor = 'blue', marker = 'o')

    ax.plot(x[0]+.01,mean_sub60_lmic, markersize=15, color='white', markeredgecolor = 'red', marker = 'o')
    ax.plot(x[1]+.01,mean_over60_lmic, markersize=15, color='white', markeredgecolor = 'red', marker = 'o')

    plt.xlim(.1,.4)

    ax.set_xticks(x)

    labels = ['<60min','>60min']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')        

    axes_limits = ax.get_ylim()

    ax.plot([x[0],x[1]],[axes_limits[1]+10,axes_limits[1]+10],color='black', lw=1)
    ax.plot([x[0]-.01,x[1]-.01],[axes_limits[1]-10,axes_limits[1]-10],color='black', lw=1)
    ax.plot([x[0]+.01,x[1]+.01],[axes_limits[1],axes_limits[1]],color='black', lw=1)

    posOne = x[1]-(x[1]-x[0])+(x[1]-x[0])/4
    posHIC = (x[1]-.01)-((x[1]-.01)-(x[0]-.01))+((x[1]-.01)-(x[0]-.01))/4
    posLMIC = (x[1]+.01)-((x[1]+.01)-(x[0]+.01))+((x[1]+.01)-(x[0]+.01))/4

    p = 'p = ' + str(np.round(p_value[1],2))
    pHIC = 'p = ' + str(np.round(p_value_hic[1],2))
    pLMIC = 'p = ' + str(np.round(p_value_lmic[1],2))

    font_size = 10

    ax.annotate(p,(posOne,axes_limits[1]+10.5),color = 'black',fontsize=font_size)
    ax.annotate(pHIC,(posHIC,axes_limits[1]-9.5),color = 'black',fontsize=font_size)
    ax.annotate(pLMIC,(posLMIC,axes_limits[1]+.5),color = 'black',fontsize=font_size)

    plt.close(SuppFig1B)

#%%
#contingency table

    lmic_sub60 = len(sub60_lmic_f[:,0])
    lmic_over60 = len(over60_lmic_f[:,0])

    hic_sub60 = len(sub60_hic_f[:,0])
    hic_over60 = len(over60_hic_f[:,0])

    table = np.array([[hic_sub60, hic_over60],[lmic_sub60, lmic_over60]])
    
    oddsr, p_fish = stats.fisher_exact(table, alternative='two-sided')                  

    cont_stats = {
                        'p-value' : p_fish,
                        'OR'       : oddsr
                 }   

    if p_fish <0.0001: 

                p_fish = str('<0.0001')

    else:
        p_fish = str(np.round(p_fish,2))

    cont_table = tabulate({'': ['HIC', 'LMIC'], 'SE <60min': [(str(hic_sub60)), (str(lmic_sub60))], 'SE >60min': [(str(hic_over60)), (str(lmic_over60))]}, headers="keys", tablefmt='fancy_grid')

    lmic_sub60_perc = np.round(len(sub60_lmic_f[:,0])/(len(sub60_lmic_f[:,0])+len(over60_lmic_f[:,0]))*100,2)
    lmic_over60_perc = np.round(len(over60_lmic_f[:,0])/(len(sub60_lmic_f[:,0])+len(over60_lmic_f[:,0]))*100,2)

    hic_sub60_perc = np.round(len(sub60_hic_f[:,0])/(len(sub60_hic_f[:,0])+len(over60_hic_f[:,0]))*100,2)
    hic_over60_perc = np.round(len(over60_hic_f[:,0])/(len(sub60_hic_f[:,0])+len(over60_hic_f[:,0]))*100,2)

    perc_table = tabulate({'': ['HIC', 'LMIC'], 'SE <60min': [(str(hic_sub60_perc)+'%'), (str(lmic_sub60_perc)+'%')], 'SE >60min': [(str(hic_over60_perc)+'%'), (str(lmic_over60_perc)+'%')]}, headers="keys", tablefmt='fancy_grid')
    
    Fig1C,ax=plt.subplots(figsize=(5,5))

    plt.title('Fig1C')

    ax.bar([.2,.3], [hic_sub60_perc,lmic_sub60_perc], color=['blue','red'], width = .05, alpha=.25)

    ax.bar([.2,.3], [hic_over60_perc,lmic_over60_perc], bottom = [hic_sub60_perc,lmic_sub60_perc],color=['white','white'], width = .05)

    ax.bar([.2,.3], [hic_over60_perc,lmic_over60_perc], bottom = [hic_sub60_perc,lmic_sub60_perc],color=['blue','red'], width = .05)

    ax.set_ylabel('Proportion of studies (%)')

    x = [.2,.3]

    labels = ['HIC','LMIC']

    ax.set_xticks(x)

    ax.set_xticklabels(labels)  

    plt.xlim(.1,.4)

    axes_limits = ax.get_ylim()

    ax.plot([x[0],x[1]],[axes_limits[1],axes_limits[1]],color='black', lw=1)

    posOne = x[1]-(x[1]-x[0])+(x[1]-x[0])/4

    font_size = 10

    p_fish = 'p = ' + p_fish

    ax.annotate(p_fish,(posOne,axes_limits[1]+.5),color = 'black',fontsize=font_size)

    ax.plot(.110,105,markersize=10,marker='s',color='black', alpha=.25)
    plt.text(.120, 103, '<60min', fontsize=12)

    ax.plot(.110, 100,markersize=10,marker='s',color='black')
    plt.text(.120, 98, '>60min', fontsize=12)

    plt.close(Fig1C)

    #%%    
    SuppFig1C,ax=plt.subplots(figsize=(5,5))

    plt.title('SuppFig1C')

    x = [.2,.3,.4]

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')

#%%
#plotting original figure with all detail (i.e. stratified across duration of SE, age of participants, number of participants and economic groups)
        
    sub30 = np.zeros(shape=(len(data),2))
    over30sub60 = np.zeros(shape=(len(data),2))
    over60 = np.zeros(shape=(len(data),2))

    total_episodes = data['episodes'].sum()

    for i in range(len(data)):
        
        group = data.state[i]
        
        episodes = data.episodes[i]
        
        weight = episodes/total_episodes*500
        
        resistance = data.resistance[i]
        
        age = data.age[i]
        
        phase = data.phase[i]
        
        marker = 'o'
        
        if age == 'paediatric':
            
            color = 'magenta'

        elif age == 'adult':
            
            color = 'green'

        elif age == 'both':
            
            color = 'black'           

        if phase == '10-30min' and group == 'HIC':
            
            sub30[i,0] = resistance
            
            sub30[i,1] = episodes
            
            ax.plot(x[0]-.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)
            ax.plot(x[0]-.015, resistance,markersize=weight, color = 'blue', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)
        
        elif phase == '10-30min' and group == 'LMIC':
            
            sub30[i,0] = resistance
            
            sub30[i,1] = episodes
            
            ax.plot(x[0]+.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)
            ax.plot(x[0]+.015, resistance,markersize=weight, color = 'red', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)
        
        elif phase == '31-60min' and group == 'HIC':
            
            over30sub60[i,0] = resistance
            
            over30sub60[i,1] = episodes
            
            ax.plot(x[1]-.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2,alpha=.2)        
            ax.plot(x[1]-.015, resistance,markersize=weight, color = 'blue', marker = marker, markeredgecolor = color, markeredgewidth=2,alpha=.2)        

        elif phase == '31-60min' and group == 'LMIC':
            
            over30sub60[i,0] = resistance
            
            over30sub60[i,1] = episodes
            
            ax.plot(x[1]+.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2,alpha=.2)               
            ax.plot(x[1]+.015, resistance,markersize=weight, color = 'red', marker = marker, markeredgecolor = color, markeredgewidth=2,alpha=.2)               
                
        elif phase == '>60min' and group == 'HIC':
            
            over60[i,0] = resistance
            
            over60[i,1] = episodes
            
            ax.plot(x[2]-.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)        
            ax.plot(x[2]-.015, resistance,markersize=weight, color = 'blue', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)        

        elif phase == '>60min' and group == 'LMIC':
            
            over60[i,0] = resistance
            
            over60[i,1] = episodes
            
            ax.plot(x[2]+.015, resistance,markersize=weight, color = 'white', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)        
            ax.plot(x[2]+.015, resistance,markersize=weight, color = 'red', marker = marker, markeredgecolor = color, markeredgewidth=2, alpha=.2)        
            
    plt.xlim(.1,.5)

    ax.plot(x[0],mean_diff_sub30, markersize=15, color='white', markeredgecolor = 'purple', marker = 'o')
    ax.plot(x[1],mean_diff_over30sub60, markersize=15, color='white', markeredgecolor = 'purple', marker = 'o')
    ax.plot(x[2],mean_diff_over60, markersize=15, color='white', markeredgecolor = 'purple', marker = 'o')

    ax.plot([x[0],x[0]],[mean_diff_sub30-sem_diff_sub30,mean_diff_sub30+sem_diff_sub30],color='purple', lw=3)
    ax.plot([x[1],x[1]],[mean_diff_over30sub60-sem_diff_over30sub60,mean_diff_over30sub60+sem_diff_over30sub60],color='purple', lw=3)
    ax.plot([x[2],x[2]],[mean_diff_over60-sem_diff_over60,mean_diff_over60+sem_diff_over60],color='purple', lw=3)

    ax.set_xticks(x)

    labels = ['10-30min','31-60min','>60min']

    ax.set_xticklabels(labels)

    ax.set_ylabel('BZP-R (%)')

    ax.plot(.125,100,markersize=10,marker='_',color='white',markeredgecolor = 'green')
    plt.text(.140, 98, 'Adult only', fontsize=12)

    ax.plot(.125,95,markersize=10,marker='_',color='white',markeredgecolor = 'magenta')
    plt.text(.140, 93, 'Paediatric only', fontsize=12)

    ax.plot(.125,90,markersize=10,marker='_',color='white',markeredgecolor = 'black')
    plt.text(.140, 88, 'Mixed', fontsize=12)

    ax.plot(.125,85,markersize=10,marker='o',color='white', markeredgecolor = 'purple')
    plt.text(.140, 83, 'Weighted Mean.', fontsize=12)

    ax.plot(.125,80,markersize=10,marker='o',color='blue')
    plt.text(.140, 78, 'HIC', fontsize=12)

    ax.plot(.125,75,markersize=10,marker='o',color='red')
    plt.text(.140, 73, 'LMIC', fontsize=12)

    plt.close(SuppFig1C)

    return(nonweighted_stats_phases_eco, weighted_stats_phases_eco, cont_table, cont_stats, perc_table, Fig1C, SuppFig1B, SuppFig1C)
