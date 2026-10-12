% transmission line equations
function zin = txline(zl, z0, bl)

gamma = (zl-z0)./(zl+z0)
zin = z0.*((zl + 1i.*z0.*tan(bl))./(z0 + 1i.*zl.*tan(bl)));
%zin = z0.*((1+(gamma.*exp(-1i.*2.*bl)))./(1-(gamma.*exp(-1i.*2.*bl))));
%zin = (1./z0).*((1-(gamma.*exp(-1i.*2.*bl)))./(1+(gamma.*exp(-1i.*2.*bl)))); % admittance