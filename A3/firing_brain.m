function grid = firing_brain(N, t_steps)
    % run: firing_brain(40, 100);
    % resting (0), ready (1), firing (2)
    grid = ones(N+2); % all neurons are ready, there's a padding for periodic boundaries
    ind = (2:N+1); % indices of actual cells
    grid(ind,ind) = ones(N) + (rand(N) < 0.3); % choose firing
    grid = boundary(grid); % apply periodic boundary
    
    for t=1:t_steps
        FN = firing_neighbours(grid); % matrix of count of firing neighbours for each cell
        new = grid + (grid ~= 1) .* ones(N+2); % update to obtain resting (0) -> ready (1), firing will turn to 3
        new = (new == 1); % keep only old and new ready, firing will turn to resting (0)
        new = new + (grid == 1) .* (FN == 2); % change ready (1) to firing (2) if neighbours == 2
        new = boundary(new); % add periodic boundaries
        grid = new; % update grid
    end
    
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
    
    % TODO
    function plot_result(M)
        R = M(ind, ind) == 1;
        [rx, ry] = get_coords(R);
        % plot(rx, ry, '.', 'MarkerSize',12);
    end

    function [x, y] = get_coords(bin_M)
        [x, y] = find(bin_M);
        disp(x);
        disp(y);
        x = x ./ (N+2);
        y = y ./ (N+2);
    end
end