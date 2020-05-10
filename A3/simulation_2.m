
m_1=zeros(1,100);
m_2=zeros(1,100);
m_3=zeros(1,100);
m_4=zeros(1,100);

p1=zeros(1,100);
p2=zeros(1,100);
p3=zeros(1,100);
p4=zeros(1,100);


%gama:An infected individual recovers with propability gamma
%propability list, we start with a p propability of infected individuals
 p=sort(rand(1,100));

for i=1:100
    
    for s=1:100
        m_1(s)=gama_p(0.6,p(i));
        m_2(s)=gama_p(0.5,p(i));
        m_3(s)=gama_p(0.4,p(i));
        m_4(s)=gama_p(0.3,p(i));
    end
    %count the number of zeros on m_1,m_2,m_3,m_4 i.e z_1,z_1,z_1,z_1
    %calc the prob of the disease dying out i.e p_1,p_2,p_3,p_4
    z_1=nnz(~m_1); p_1=z_1/100; p1(i)=p_1;
    z_2=nnz(~m_2); p_2=z_2/100; p2(i)=p_2;
    z_3=nnz(~m_3); p_3=z_3/100; p3(i)=p_3;
    z_4=nnz(~m_4); p_4=z_4/100; p4(i)=p_4;
  
end
    %gamas=[0.3, 0.4, 0.5, 0.6];
    %means=[m1,m2,m3,m4];

%figure
hold on
mp1=plot(p1,'LineWidth', 2);
mp2=plot(p2,'LineWidth', 2);
mp3=plot(p3,'LineWidth', 2);
mp4=plot(p4,'LineWidth', 2);
xlabel('');
ylabel('propability of the disease dying out')
hold off
set(gca,'FontSize',18);
h = [mp1(1);mp2;mp3(1);mp4];
legend(h,'gamma=0.6','gamma=0.5','gamma=0.4','gamma=0.3');


