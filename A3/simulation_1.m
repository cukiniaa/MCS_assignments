p1=gama(0.3);
p2=gama(0.4);
p3=gama(0.5);
p4=gama(0.6);

v1=plot(p1);
hold on
v2=plot(p2);
v3=plot(p3);
v4=plot(p4);
xlabel('Time interval (days)');
ylabel('Propability of infection');

m_1=zeros(1,100);
m_2=zeros(1,100);
m_3=zeros(1,100);
m_4=zeros(1,100);

for s=1:100
    m_1(s)=mean2(gama(0.3));
    m_2(s)=mean2(gama(0.4));
    m_3(s)=mean2(gama(0.5));
    m_4(s)=mean2(gama(0.6));
end
m1=mean2(m_1);
m2=mean2(m_2);
m3=mean2(m_3);
m4=mean2(m_4);

gamas=[0.3, 0.4, 0.5, 0.6];
means=[m1,m2,m3,m4];
figure
plot(gamas,means);
xlabel('gamma Values');
ylabel('Propability of Infection')

figure
subplot(4,1,1); 
histogram(m_1);
set(ylabel('number of infections'),'Rotation',90);
xlabel('propability of infection, gamma=0.3');
subplot(4,1,2);
histogram(m_2);
set(ylabel('number of infections'),'Rotation',90);
xlabel('propability of infection, gamma=0.4');
subplot(4,1,3);
histogram(m_3);
set(ylabel('number of infections'),'Rotation',90);
xlabel('propability of infection, gamma=0.5');
subplot(4,1,4);
histogram(m_4);
set(ylabel('number of infections'),'Rotation',90);
xlabel('propability of infection, gamma=0.6');
hold off

h = [v1(1);v2;v3(1);v4];
legend(h,'gama 0.3','gama 0.4','gama 0.5','gama 0.6');




