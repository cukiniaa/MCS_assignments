e=sort(rand(1,100)); %noise generator
J=100; %Number of timestep t0 be use
p=zeros(1,length(e)); %array to hold the polarization values on the last time step of the implementation

for i=1:1:length(e)
    p(i)=Polarization(e(i),J);
end


plot(e,p,'LineWidth', 2);
xlabel('Noise parameter');
set(gca,'xlim',[0,1]);
ylabel('Polarisation of particles')
hold off
set(gca,'FontSize',14);