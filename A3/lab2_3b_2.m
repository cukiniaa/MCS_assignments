p1=gama_p(0.3,0.6);
p2=gama_p(0.4,0.6);
p3=gama_p(0.5,0.6);
p4=gama_p(0.6,0.6);

v1=plot(p1);
hold on
v2=plot(p2);
v3=plot(p3);
v4=plot(p4);
xlabel('Time interval (days)');
ylabel('Propability of infection,p=0.6');

m_1=zeros(1,100);
m_2=zeros(1,100);
m_3=zeros(1,100);
m_4=zeros(1,100);
m_1_a=zeros(1,100);
m_2_a=zeros(1,100);
m_3_a=zeros(1,100);
m_4_a=zeros(1,100);
m_1_b=zeros(1,100);
m_2_b=zeros(1,100);
m_3_b=zeros(1,100);
m_4_b=zeros(1,100);
m_1_c=zeros(1,100);
m_2_c=zeros(1,100);
m_3_c=zeros(1,100);
m_4_c=zeros(1,100);

%p=0.6
for s=1:100
    m_1(s)=mean2(gama_p(0.3,0.6));
    m_2(s)=mean2(gama_p(0.4,0.6));
    m_3(s)=mean2(gama_p(0.5,0.6));
    m_4(s)=mean2(gama_p(0.6,0.6));
end
m1=mean2(m_1);
m2=mean2(m_2);
m3=mean2(m_3);
m4=mean2(m_4);
gamas=[0.3, 0.4, 0.5, 0.6];
means=[m1,m2,m3,m4];

%p=0.5
for s=1:100
    m_1_a(s)=mean2(gama_p(0.3,0.5));
    m_2_a(s)=mean2(gama_p(0.4,0.5));
    m_3_a(s)=mean2(gama_p(0.5,0.5));
    m_4_a(s)=mean2(gama_p(0.6,0.5));
end
m1_a=mean2(m_1_a);
m2_a=mean2(m_2_a);
m3_a=mean2(m_3_a);
m4_a=mean2(m_4_a);
means_a=[m1_a,m2_a,m3_a,m4_a];

%p=0.4
for s=1:100
    m_1_b(s)=mean2(gama_p(0.3,0.4));
    m_2_b(s)=mean2(gama_p(0.4,0.4));
    m_3_b(s)=mean2(gama_p(0.5,0.4));
    m_4_b(s)=mean2(gama_p(0.6,0.4));
end
m1_b=mean2(m_1_b);
m2_b=mean2(m_2_b);
m3_b=mean2(m_3_b);
m4_b=mean2(m_4_b);
means_b=[m1_b,m2_b,m3_b,m4_b];

%p=0.3
for s=1:100
    m_1_c(s)=mean2(gama_p(0.3,0.3));
    m_2_c(s)=mean2(gama_p(0.4,0.3));
    m_3_c(s)=mean2(gama_p(0.5,0.3));
    m_4_c(s)=mean2(gama_p(0.6,0.3));
end
m1_c=mean2(m_1_c);
m2_c=mean2(m_2_c);
m3_c=mean2(m_3_c);
m4_c=mean2(m_4_c);
means_c=[m1_b,m2_b,m3_b,m4_b];




figure
hold on
mp1=plot(gamas,means);
mp2=plot(gamas,means_a);
mp3=plot(gamas,means_b);
mp4=plot(gamas,means_c);
xlabel('gamma Values');
ylabel('Mean Value of propability of Infection')
hold off
h = [mp1(1);mp2;mp3(1);mp4];
legend(h,'p=0.6','p=0.5','p=0.4','p=0.3');


figure
subplot(4,1,1); 
histogram(m_1);
set(ylabel('number of infections'),'Rotation',90);
xlabel('propability of infection, gamma=0.3, p=0.6');
subplot(4,1,2);
histogram(m_2);
set(ylabel('number of infections'),'Rotation',90);
xlabel('propability of infection, gamma=0.4,p=0.6');
subplot(4,1,3);
histogram(m_3);
set(ylabel('number of infections'),'Rotation',90);
xlabel('propability of infection, gamma=0.5,p=0.6');
subplot(4,1,4);
histogram(m_4);
set(ylabel('number of infections'),'Rotation',90);
xlabel('propability of infection, gamma=0.6,p=0.6');
hold off


h = [v1(1);v2;v3(1);v4];
legend(h,'gama 0.3','gama 0.4','gama 0.5','gama 0.6');

