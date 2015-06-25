#-------------------------------------------------------------
#Basic chik(k,w) calculation.
#Based on the MATLAB script kw.m 
#2015 Dan Elton
#-------------------------------------------------------------
from pylab import *
from scipy import optimize 
from numpy import *

data = loadtxt('../../eps_k/TIP4P2005f_512_300HR8ns_phikL_raw.dat')
data2 = loadtxt('../../eps_k/TIP4P2005f_512_300HR8ns_chik_raw.dat')

ntimesteps = size(data,0)
num_points = 1000
printdata  = 0

#initialize arrays 
Nk = size(data,1) - 1

times_ps = data[:,0]
timestep = times_ps[1] - times_ps[0]  
times_ps = linspace(0,ntimesteps,1)*timestep

corr_funs = data[:,1:size(data,1)]
k_values  = data2[:,0]
chik0     = data2[:,1] 

temp  = zeros(num_points,dtype=complex64)
freqs = zeros(num_points)
chikw = zeros([num_points, Nk])
 
num_avg_over = floor(ntimesteps/num_points)
nextpow2 = int(2**ceil(log2(ntimesteps)))
f = array(range(0,ntimesteps,1))/(timestep*nextpow2) #Frequency range
 
for k in range(Nk):
	tderiv = diff(corr_funs[:,k])/timestep

        y = fft.ifft(tderiv,nextpow2)  
            
        #reduce number of points in data by averaging over blocks
        for i in xrange(1,num_points-1):
		temp[i-1]  = mean( y[(i-1)*num_avg_over : i*num_avg_over] )

        chikw[:,k] = -chik0[k]*imag(temp) 
	print k
	
for i in xrange(1,num_points-1):
	freqs[i-1] = mean( f[(i-1)*num_avg_over : i*num_avg_over] )

freqs_cm = 33.44*freqs #Convert freqs to inverse centimeters

data_2_plot = chikw[:,0:18:2]

legendvalues = []

for i in range(0,18,2):
	legendvalues = legendvalues + ['%4.2f' % k_values[i]]
 
#set(gca,'ColorOrder', jet(i))
 #set(gca,'FontSize',30)
#ylabel("\chi''_L (k,\omega)","FontSize",35) 
#xlabel('\omega (cm^{-1})','FontSize',35)
#title('\omega (THz)','FontSize',35);
plot(freqs_cm, data_2_plot) 

legend(legendvalues)


show()
#set(gcf, 'Position', [0 1 1100 820])  %size


#max_freq2plot = 2100;
#xlim(gca,[0 max_freq2plot]);
#%  ylim(gca,[-5 25]);
#ylim(gca,[-1.5 100]);  %L

#% ylim(gca,[-3 13]); %T

#set(gca, 'XScale', 'Linear','Xtick',(0:500:max_freq2plot),'Ytick',zeros(1,0));
#first_axis = gca;
#sqz = 0.12; %// distance to squeeze the first plot
#% set(first_axis, 'Position', get(first_axis, 'Position'));
#ax2 = axes('Position', get(first_axis, 'Position'),'Color','none','XAxisLocation','top','YTick',zeros(1,0));
#scale_factor = 0.02998; %// change this to your satisfaction
#xlim(get(first_axis, 'XLim') * scale_factor);
#set(ax2, 'XScale', get(first_axis, 'XScale'));  
#set(ax2,'FontSize',30)
#set(ax2,'FontSize',30)
#set(ax2,'ytick',[],'ycolor',[0 0 0],'YAxisLocation','right');

#annotation(gcf,'textbox',...
    #[0.908177033492824 0.945169712793734 0.10522009569378 0.0509138381201044],...
    #'String',{'k (A^{-1})'},...
    #'FontSize',28,...
    #'FitBoxToText','off',...
    #'EdgeColor',[1 1 1],...
    #'BackgroundColor',[1 1 1]);








