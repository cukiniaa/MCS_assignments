function [P]=gama(g)
 N=100; %number of individuals
 T=100; %time interval
 I=1; %infected
 S=0; %susceptible
    
p=zeros(1,N+2); %hold the population and the boundaries

%initial condition
p(2:N+1)=S;
p((N+2)/2)=I; 

%toroidal boundary
p(1)=p(N+1);
p(N+2)=p(2);
pnew=p;

P=zeros(1,T); %prob of infection in each time level

for t=1:T
    for i=2:N+1
       
        if  p(i)==I 
            x=rand;
            if x<g %infected becomes S with prob g
                pnew(i)=S;
            
            else
                pnew(i)=I; %otherwise stays infected
            end
        end
        
        if p(i)==S && (p(i-1)==I || p(i+1)==I ) %if S and neighbour is I ,becomes I with probability 1-gamma
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
    P(t)=(sum(p(2:N+1)==1))/N; %in each time step calc the probability of the disease spreading and store it
 end


end
