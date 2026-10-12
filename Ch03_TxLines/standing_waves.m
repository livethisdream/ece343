% Standing waves
B = 0:pi/10:6*pi;
refl0 = 0.25;
refl = 0.5;
refl2 = 0.75;
V0=1;
phi=0;

Vp0 = V0*sqrt(1 + refl0.^2 +(2*refl0)*cos(B + phi));
Vp1 = V0*sqrt(1 + refl.^2 +(2*refl)*cos(B + phi));
Vp2 = V0*sqrt(1 + refl2.^2 +(2*refl2)*cos(B + phi));

figure;
plot(B,Vp1, B, Vp2, B, Vp0)