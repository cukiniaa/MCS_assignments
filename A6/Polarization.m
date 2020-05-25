function P=Polarization(e,J)
% Fixed number of particles N
% Fixed radius L
% e: Noise parameter
% J: Number of timestep t0 be used

 N=40;
 L=20; 
 r=1;
 
 %position
 x=zeros(N,J+1); % x(i,j) gives the x coordinate of the ith particle at time j
 x(:,1)=L*rand(N,1); %define initial x coordiantes of all particles
 
 y=zeros(N,J+1); % y(i,j) gives the y coordinate of the ith particle at time j
 y(:,1)=L*rand(N,1); %define initial y coordiantes of all particles
 
 T=zeros(N,J+1); % T(i,j) gives the angle with the x axis of the direction of motion of the ith % particle at time j
 T(:,1)=2*pi*rand(N,1); %define initial direction of all particles
 
 
 %For all time steps
 for j=1:J
    %For each particle
    for i=1:N
            %finds how many particles are in the interaction radius of each
            %particle
            A(:,1)=((x(i,j)-x(:,j)).^2+(y(i,j)-y(:,j)).^2).^0.5<=r;
            A(:,2)=((x(i,j)-x(:,j)-L).^2+(y(i,j)-y(:,j)).^2).^0.5<=r;
            A(:,3)=((x(i,j)-x(:,j)).^2+(y(i,j)-y(:,j)-L).^2).^0.5<=r;
            A(:,4)=((x(i,j)-x(:,j)+L).^2+(y(i,j)-y(:,j)).^2).^0.5<=r;
            A(:,5)=((x(i,j)-x(:,j)).^2+(y(i,j)-y(:,j)+L).^2).^0.5<=r;
            A(:,6)=((x(i,j)-x(:,j)+L).^2+(y(i,j)-y(:,j)+L).^2).^0.5<=r;
            A(:,7)=((x(i,j)-x(:,j)+L).^2+(y(i,j)-y(:,j)-L).^2).^0.5<=r;
            A(:,8)=((x(i,j)-x(:,j)-L).^2+(y(i,j)-y(:,j)+L).^2).^0.5<=r;
            A(:,9)=((x(i,j)-x(:,j)-L).^2+(y(i,j)-y(:,j)-L).^2).^0.5<=r;
        
            B=sum(A')';         
            ss=sum(sin(T(:,j)).*B)/sum(B);
            sc=sum(cos(T(:,j)).*B)/sum(B);
            S=atan2(ss,sc);
                   
            T(i,j+1)=S+e*(rand-0.5); %adds noise to the measured angle
            
    end
 end
 
 %Calculate the polarisation of particles at the last time step
 P=(1/N)*sqrt( (sum(sin(T(:,j+1))))^2 + (sum(cos(T(:,j+1))))^2 );
           
 
end
