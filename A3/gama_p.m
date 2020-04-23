function [P]=gama_p(g,pr)
 N=100; 
 T=100; 
 I=1;
 S=0;
 R=0.5;
 %g=0.6;
 %pr=0.6;

 p=zeros(1,N+2);
 p(2:N+1)=sprand(1,N,pr);
 %full(p)
 p=p~=0;
 %full(p)
 p=double(p);
 %p(2:N+1)

 %toroidal boundary
 p(1)=p(N+1);
 p(N+2)=p(2);
 pnew=p;

 %full(p(2:N+1))

 Inf=zeros(1,T); %data list to store infectious in each time level
 P=zeros(1,T); %prob of infection in each time level

for t=1:100
    for i=2:N+1
       
        if  p(i)==I 
            x=rand;
            if x<g %infected recovers with prob gamma
                pnew(i)=R;
            
            else
                pnew(i)=I; %otherwise stays infected
            end
        end
        
        if p(i)==S && (p(i-1)==I || p(i+1)==I ) %if S and neighbour is I --> becomes I with prob 1-g
         
            x=rand;
            if x<1-g
                pnew(i)=I;
            else
                pnew(i)=S;
            end
        end
            
     end
        
 %end  
    
    p(2:N+1)=pnew(2:N+1);
    p(1)=p(N+1);
    p(N+2)=p(2);
    %full(p(2:N+1))
    
    Inf(t)=sum(p(2:N+1)==1);   %in each time step count the Infectious and store them in the infectious list
    P(t)=(sum(p(2:N+1)==1))/N; %in each time step calc the probability of the disease spreading and store in
end
  %full(p(2:N+1))
end

