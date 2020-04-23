function result = firing_brain(N, t_steps, graphics, ptime)
% N - size of the problem
% t_steps - number of steps
% graphics - if enable plot then 1 otherwise 0
% ptime - how long a step should be displayed on the plot
% example: firing_brain(40, 100, 1, 1);
% states: resting (0), ready (1), firing (2)

    grid = ones(N+2); % all neurons are ready, there's a padding for periodic boundaries
    ind = (2:N+1); % indices of actual cells
    grid(ind,ind) = ones(N) + (rand(N) < 0.3); % choose firing
    grid = boundary(grid); % apply periodic boundary

    mid = ceil(N / 2); % for plotting the grid
    if(graphics == 1)
        pause on
        plot_result(grid);
    end

    for t=1:t_steps
        FN = firing_neighbours(grid); % matrix of count of firing neighbours for each cell
        new = grid + (grid ~= 1) .* ones(N+2); % update to obtain resting (0) -> ready (1), firing will turn to 3
        new = (new == 1); % keep only old and new ready, firing will turn to resting (0)
        new = new + (grid == 1) .* (FN == 2); % change ready (1) to firing (2) if neighbours == 2
        new = boundary(new); % add periodic boundaries
        grid = new; % update grid
        if(graphics == 1)
            pause(ptime);
            plot_result(grid);
        end
    end

    result = grid(ind, ind);

    function M = boundary(M)
        M(1,:) = M(N+1, :);
        M(N+2,:) = M(2,:);
        M(:,1) = M(:,N+1);
        M(:,N+2) = M(:,2);
        M(1,1) = M(N+1,N+1);
        M(N+2,N+2) = M(2,2);
        M(1,N+2) = M(N+1,2);
        M(N+2,1) = M(2,N+1);
    end

    function FN = firing_neighbours(M)
        F = (M == 2); % 1 -> firing, otherwise 0
        FN = zeros(N+2);
        FN(ind, ind) = F(1:end-2, 2:end-1) + F(3:end, 2:end-1) ... % up and down
                + F(2:end-1, 1:end-2) + F(2:end-1, 3:end) ... % left and right
                + F(1:end-2, 1:end-2) + F(1:end-2, 3:end) ... % left-up and right-up
                + F(3:end, 1:end-2) + F(3:end, 3:end); % left-down and right-down
    end

    function plot_result(grid)
        M = grid(ind, ind);
        [ready_x, ready_y] = get_coords(M == 1);
        [resting_x, resting_y] = get_coords(M == 0);
        [firing_x, firing_y] = get_coords(M == 2);
        plot(ready_x, ready_y, '.', 'MarkerSize', 40, 'Color', '#0072BD'); % blue
        hold on
        plot(resting_x, resting_y, 'o', 'MarkerSize', 12, 'Color', '#0072BD'); % not filled
        plot(firing_x, firing_y, '.', 'MarkerSize', 40, 'Color', '#77AC30'); % green
        hold off
        axis([-(N+1)*0.1 (N+1)*0.1 -(N+1)*0.1 (N+1)*0.1]);
        set(gca,'xtick',[]);
        set(gca,'ytick',[]);
    end

    function [x, y] = get_coords(bin_M)
        [rx, ry] = find(bin_M);
        y = (mid - rx) * 0.1;
        x = (ry - mid) * 0.1;
    end
end