% This script tests our SEIR model for different values of
% parameters gamma, beta and kappa. It plots percentage of
% affected individuals for different values of the parameters.

t_steps = 350;
n_tries = 100;
N = 40;
d = 0.01;
population = N * N;

% --------------- GAMMA -----------------
gammas = [0.1, 0.12, 0.14, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.7];
kappa = 0.7;
beta = 0.6;

g_affected = zeros(1, length(gammas));

for i = 1:length(gammas)
    gamma = gammas(i);
    for j=1:n_tries
        [res, inf] = SIRT_2(N, t_steps, d, gamma, kappa, beta, 0, 0); 
        g_affected(i) = g_affected(i) + nnz(res ~= 0);
    end
end
g_affected = (g_affected / n_tries) / population * 100;

figure(1);
plot(gammas, g_affected, 'LineWidth', 2);
xlabel('\gamma');
ylabel('% Affected');
set(gca,'FontSize',18);

%--------------- BETA -----------------
betas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1];
kappa = 0.7;
gamma = 0.22;

b_affected = zeros(1, length(betas));
b_infected = zeros(1, length(betas));

for i = 1:length(betas)
    beta = betas(i);
    for j=1:n_tries
        [res, inf] = SIRT_2(N, t_steps, d, gamma, kappa, beta, 0, 0); 
        b_affected(i) = b_affected(i) + nnz(res ~= 0);
        b_infected(i) = b_infected(i) + ((nnz(res == 1) + nnz(res == 2)) == 0);
    end
end
b_affected = (b_affected / n_tries) / population * 100;
b_infected = b_infected / n_tries;

figure(2);
plot(betas, b_affected, 'LineWidth', 2);
xlabel('\beta');
ylabel('% Affected');
set(gca,'FontSize',18);

% --------------- KAPPA -----------------
kappas = [0.01, 0.1, 0.2, 0.3, 0.4,  0.5, 0.7, 0.8];
gamma = 0.2;
beta = 0.6;

k_affected = zeros(1, length(kappas));

for i = 1:length(kappas)
    kappa = kappas(i);
    for j=1:n_tries
        [res, inf] = SIRT_2(N, t_steps, d, gamma, kappa, beta, 0, 0); 
        k_affected(i) = k_affected(i) + nnz(res ~= 0);
    end
end
k_affected = (k_affected / n_tries) / population * 100;

figure(3);
plot(kappas, k_affected, 'LineWidth', 2);
xlabel('\kappa');
ylabel('% Affected');
set(gca,'FontSize',18);