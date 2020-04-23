N = 40;
t_step = 1000;
n_tries = 100;
f_sum = zeros(t_step+1, 1);

for i=1:n_tries
   [res, f] = firing_brain(N, t_step, 0);
   f_sum = f_sum + f;
end

f_avg = f_sum / n_tries;

plot([0:t_step], f_avg, 'LineWidth', 2);

xlabel('Time steps')
ylabel('Number of firing cells');
set(gca,'FontSize',18);