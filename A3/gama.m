function [P]=gama(g)
 N=100; %number of individuals
 T=100; %time interval
 I=1;
 R=0;
 S=0.5;
    
p=zeros(1,N+2);

%initial condition
p(2:N+1)=S;
p((N+2)/2)=I;

%toroidal boundary
p(1)=p(N+1);
p(N+2)=p(2);
pnew=p;

Inf=zeros(1,T); %data list to store infectious in each time level
P=zeros(1,T); %prob of infection in each time level

for t=1:T
    for i=2:N+1
       
        if  p(i)==I 
            x=rand;
            if x<g %infected recovers with prob gamma
                pnew(i)=R;
            
            else
                pnew(i)=I; %otherwise stays infected
            end
        end
        
        if p(i)==S && (p(i-1)==I || p(i+1)==I ) %if S and neighbour is I --> becomes I with probability 1-gamma
            x=rand;
            if x<1-g
                pnew(i)=I;
            else
                pnew(i)=S;
            end
        end
        
    end  
    
    p(2:N+1)=pnew(2:N+1);
    p(1)=p(N+1);
    p(N+2)=p(2);
    
    
    Inf(t)=sum(p(2:N+1)==1);   %in each time step count the Infectious and store them in the infectious list
    P(t)=(sum(p(2:N+1)==1))/N; %in each time step calc the probability of the disease spreading and store in
 end
 


end
