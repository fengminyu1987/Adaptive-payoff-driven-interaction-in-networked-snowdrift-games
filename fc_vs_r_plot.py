import matplotlib.pyplot as plt


# c_heat =  [[1, 1, 0.8085, 0.88225],
#     [0.97525, 0.921625, 0.938125, 0.84825],
#     [0.8105, 0.82, 0.78, 0.72925],
#     [0.660125, 0.687416667, 0.61, 0.616875],
#     [0.50725, 0.573, 0.51, 0.50625],
#     [0.376583333, 0.464916667, 0.37175, 0.402625],
#     [0.237, 0.361, 0.2775, 0.3],
#     [0.125, 0.244, 0.197, 0.215375],
#     [0.0135625, 0.1398125, 0.0555, 0.12475],
#     [0, 0, 0.004375, 0.0555],
#     [0, 0, 0.014, 0.005]]

c_heat = [[1, 1, 0.956, 0.951125],
    [0.9785, 0.916875, 0.975, 0.984875],
    [0.813, 0.806, 0.885, 0.8905],
    [0.6569375, 0.6883125, 0.698375, 0.691],
    [0.512, 0.573, 0.529875, 0.539375],
    [0.362, 0.464375, 0.373625, 0.374],
    [0.24, 0.347, 0.2, 0.199625],
    [0.1209375, 0.25, 0.065, 0.053375],
    [0.019, 0.128, 0.01, 0.01175],
    [0, 0.02075, 0.002, 0.002],
    [0, 0, 0.00375, 0.00375]]

x = [ 0.1*i for i in range(len(c_heat))]
y=[]

for i in range(0,len(c_heat[0])):
    y0=[]
    for j in range(len(c_heat)):
        y0.append(c_heat[j][i])
    y.append(y0)


plt.figure(dpi=600)
plt.plot(x, y[0],marker='o',markersize=6, linewidth=2, label="adaptation($k=4$)", color='red')
plt.plot(x, y[1],marker='o',markersize=6, linewidth=2, label="adaptation($k=10$)", color='black')
plt.plot(x, y[2],marker='v',markersize=6, linewidth=2, label="static($k=4$)",linestyle = '--', color='red')
plt.plot(x, y[3],marker='v',markersize=6, linewidth=2, label="static($k=10$)",linestyle = '--', color='black')



#plt.plot(x, cooperators_changes_random[2], label="r = 5.0",linestyle = ':', color='dodgerblue')
#plt.plot(x, y[4],marker='o',markersize=8, linewidth=2.5, label="$r_a$ = 1.8", color='mediumblue')
#plt.plot(x, cooperators_changes_random[3], label="r = 5.1",linestyle = ':', color='mediumblue')
#plt.plot(x, y[5],marker='o',markersize=8, linewidth=2.5, label="$r_a$ = 2.4", color='mediumspringgreen')
#plt.plot(x, cooperators_changes_random[4], label="r = 5.2",linestyle = ':', color='mediumspringgreen')
#plt.plot(x, y[6],marker='o',markersize=8, linewidth=2.5, label="$r_a$ = 3.0", color='tan')

#


plt.legend(frameon=False,loc=(1,1),bbox_to_anchor=(0.55,0.65),fontsize=11,ncol=1)

plt.xlabel('r',fontsize=15)
plt.ylabel('$f_c$',fontsize=16,rotation=0,labelpad=10)
plt.tick_params(axis='both')
#plt.yticks(np.arange(0,1600,100))
plt.yticks(size=15)
#plt.xticks(np.arange(1,2.51,0.3),size=20)
plt.xticks(size=15)
# plt.grid(True)
plt.show()

