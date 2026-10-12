clear all;
close all;

% change these
vo = 1;
zlim = 10;
tmax = 5;
alpha = 0.5;
beta = 2*2*pi; % convenient, sets wavelength to 1m
f=1; % convenient
moviereps = 1;
wavedir = 3;

% start calculating
t=linspace(0,tmax,100);
t=t(:); 
z=linspace(0,zlim,1000);
w = 2*pi*f;

switch wavedir 
    case 1 % forward
        vzt = vo.*exp(-alpha.*z).*cos((w.*t) - (beta.*z)); % each row is a new t, each col is a z value 
        vlim = vo;
    case 2 % reverse
        vzt = vo.*exp(alpha.*z).*cos((w.*t) + (beta.*z)); % each row is a new t, each col is a z value 
        vlim = 10*vo;
    case 3 % both
        vzt = vo.*exp(-alpha.*z).*cos((w.*t) - (beta.*z))+ vo.*exp(alpha.*z).*cos((w.*t) + (beta.*z)); % each row is a new t, each col is a z value 
        vlim = 10*vo;
end

figure;
hold on;
title(['V(z,t) on a Tx Line']);
for k=1:length(t)
    myplot=plot(z,vzt(k,:), 'blue', 'DisplayName',['t = ' num2str(t(k)) ' s']);
    legend('show','Location','northeastoutside')
    xlim([0 zlim])
    ylim([-vlim vlim])
    Vtotal(k)=getframe(gcf);
    delete(myplot);
end

close all;

fig=figure();
movie(fig,Vtotal,moviereps,60)
