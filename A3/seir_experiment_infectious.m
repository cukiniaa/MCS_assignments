% This script tests our SEIR model for different values of
% parameters gamma, beta and kappa. It plots number of infectious
% throughout time.

t_steps = 100;
n_tries = 500;
N = 40;
d = 0.01;

% --------------- GAMMA -----------------
gammas = [0.1, 0.12, 0.14, 0.2, 0.3, 0.5];
kappa = 0.7;
beta = 0.6;

g_recovered = zeros(1, length(gammas));

figure(1); clf(1);
hold on
for i = 1:length(gammas)
    infectious = zeros(1, t_steps+1);
    gamma = gammas(i);
    for j=1:n_tries
        [res, inf] = SIRT_2(N, t_steps, d, gamma, kappa, beta, 0, 0); 
        infectious = infectious + inf;
        g_recovered(i) = g_recovered(i) + nnz(res ~= 0);
    end
    infectious = infectious / n_tries;
    plot(infectious(2:end), 'LineWidth', 2);
end
hold off

g_recovered = g_recovered / n_tries;

xlim([1 t_steps]);
labels = arrayfun(@(x) ("\gamma = " + num2str(x)), gammas, 'UniformOutput', false);
legend(labels);
xlabel('Time');
ylabel('Number of infectious');
set(gca,'FontSize',18);

% --------------- BETA -----------------
betas = [0.3, 0.5, 0.7, 0.8, 0.9, 1];
kappa = 0.7;
gamma = 0.2;

b_affected = zeros(1, length(betas));

figure(2); clf(2);
hold on
for i = 1:length(betas)
    infectious = zeros(1, t_steps+1);
    beta = betas(i);
    for j=1:n_tries
        [res, inf] = SIRT_2(N, t_steps, d, gamma, kappa, beta, 0, 0); 
        infectious = infectious + inf;
        b_affected(i) = b_affected(i) + nnz(res ~= 0);
    end
    infectious = infectious / n_tries;
    plot(infectious(2:end), 'LineWidth', 2);
end
hold off

b_affected = b_affected / n_tries;

xlim([1 t_steps]);
labels = arrayfun(@(x) ("\beta = " + num2str(x)), betas, 'UniformOutput', false);
legend(labels);
xlabel('Time');
ylabel('Number of infectious');
set(gca,'FontSize',18);

% --------------- KAPPA -----------------
kappas = [0.1, 0.2, 0.3, 0.5, 0.7];
gamma = 0.2;
beta = 0.6;

t_steps = 300;

k_recovered = zeros(1, length(kappas));

figure(3); clf(3);
hold on
for i = 1:length(kappas)
    infectious = zeros(1, t_steps+1);
    kappa = kappas(i);
    for j=1:n_tries
        [res, inf] = SIRT_2(N, t_steps, d, gamma, kappa, beta, 0, 0); 
        infectious = infectious + inf;
        k_recovered(i) = k_recovered(i) + nnz(res ~= 0);
    end
    infectious = infectious / n_tries;
    plot(infectious(2:end), 'LineWidth', 2);
end
hold off

k_recovered = k_recovered / n_tries;

xlim([1 t_steps]);
labels = arrayfun(@(x) ("\kappa = " + num2str(x)), kappas, 'UniformOutput', false);
legend(labels);
xlabel('Time');
ylabel('Number of infectious');
set(gca,'FontSize',18);