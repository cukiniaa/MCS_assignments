% states: S (0), E(1), I(2), R(3)
% S (susceptible) -> E (exposed, infected but not spreading yet) -> I (infectious, and spread) -> R
function result=SIRT_2(N, t_steps,d,gamma,kappa, beta,graphics,ptime)

    %N:number of Individuals
    %t_steps: Number of Simulations
    %d:We start with randomly placed Infected (I) with density d
    %gamma: An infected (I) recovers (R) with probability gamma
    %gamma: An infected becomes a transmitter (T) with probability 1-gamma
    %graphics: if enable plot then 1 otherwise 0
    %ptime - how long a step should be displayed on the plot
    %example : SIRT_2(4,10,0.2,0.4,0.4,0.4,1,1)
    
    ind=(2:N+1); %the actual cells
    grid=zeros(N+2);
    new=zeros(N+2);
    grid(ind,ind)=2*(rand(N) < d); 
    grid=boundary(grid); %apply boundary 
    
    global mid;
    mid = ceil(N / 2); % for plotting the grid
    axis_lim = [-(mid+1+mod(N, 2))*0.1 (mid+2)*0.1 -(mid+2)*0.1 (mid+1+mod(N, 2))*0.1];
    if(graphics == 1)
        pause on
        plot_result(grid);
    end

    for t=1:t_steps
        IN=Infected_neighbours(grid); %take the infected (2) neighbours of each cell
        I_R = (grid(ind,ind) == 2).*(rand(N) < gamma); % from infectious (I) to recovered (R)
        E_I = (grid(ind,ind) == 1).*(rand(N) < kappa); % are (E) now -> the become (I) 
        new(ind,ind) = grid(ind,ind) + I_R + E_I; % update the (I) to be (R) and (E) to be (I) the grid
        new(ind,ind) = new(ind,ind) + (grid(ind,ind) == 0) .* (IN(ind,ind) > 2) .* (rand(N) < beta); % change S to I if there are more than 1 (I) neighbours
        new = boundary(new); % apply boundary
        grid=new; % update grid
        if(graphics == 1)
            pause(ptime);
            plot_result(grid);
        end
    end

    result=grid(ind,ind);

    function IN=Infected_neighbours(M)
        I = (M==2);
        IN = zeros(N+2);
        IN(ind,ind)=  I(1:end-2, 2:end-1) + I(3:end, 2:end-1) ... % up and down
                    + I(2:end-1, 1:end-2) + I(2:end-1, 3:end) ... % left and right
                    + I(1:end-2, 1:end-2) + I(1:end-2, 3:end) ... % left-up and right-up
                    + I(3:end, 1:end-2) + I(3:end, 3:end);        % left-down and right-down
    end
    



    function M = boundary(M)
        %global N;
        M(1,:) = M(N+1, :);
        M(N+2,:) = M(2,:);
        M(:,1) = M(:,N+1);
        M(:,N+2) = M(:,2);
        M(1,1) = M(N+1,N+1);
        M(N+2,N+2) = M(2,2);
        M(1,N+2) = M(N+1,2);
        M(N+2,1) = M(2,N+1);
    end

    function plot_result(grid)
        M = grid(ind, ind);
        [I_x, I_y] = get_coords(M == 2);
        [S_x, S_y] = get_coords(M == 0);
        [R_x, R_y] = get_coords(M == 3);
        [E_x, E_y] = get_coords(M == 1);
        plot(I_x, I_y, '.', 'MarkerSize', 40, 'Color', 'red'); % red
        hold on
        plot(S_x, S_y, '.', 'MarkerSize', 40, 'Color', 'blue'); % blue
        plot(R_x, R_y, '.', 'MarkerSize', 40, 'Color', '#77AC30'); % green
        plot(E_x, E_y, '.', 'MarkerSize', 40, 'Color', '#D95319'); % orange
        hold off
        axis(axis_lim);
        set(gca,'xtick',[]);
        set(gca,'ytick',[]);
    end

    function [x, y] = get_coords(bin_M)
        [rx, ry] = find(bin_M);
        y = (mid - rx) * 0.1;
        x = (ry - mid) * 0.1;
    end
end