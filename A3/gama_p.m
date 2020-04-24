function [Inf]=gama_p(g,pr)
 N=100; 
 T=100; 
 I=1;
 S=0;

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

 %Inf=zeros(1,T); %data list to store infectious in each time level
 %P=zeros(1,T); %prob of infection in each time level

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
        
        if p(i)==S && (p(i-1)==I || p(i+1)==I ) %if S and neighbour is I --> becomes I with prob 1-g
         
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
    %full(p(2:N+1))
    
    %Inf(t)=sum(p(2:N+1)==1);   %in each time step count the Infectious and store them in the infectious list
    %P(t)=(sum(p(2:N+1)==1))/N; %in each time step calc the probability of the disease spreading and store in
end
   Inf=sum(p(2:N+1)==1);
  %full(p(2:N+1))
end

