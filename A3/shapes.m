
%%%% (a) moves forward at a rate one cell per time step, while preserving
%%%% the same shape
A = ones(10);
A(5,5) = 2; A(6,5) = 2;
A(4,6) = 2; A(7, 6) = 2;
firing_brain(10, 10, 1, 10, A);

%%%% (b) moves forward at a rate one cell per time step, launching
%%%% other shapes behind them
N = 10; mid = ceil(N/2);
B = ones(N);
B(mid,mid) = 2; B(mid+1,mid) = 2;
% firing_brain(N, 2, 1, 10, B);

%%%% (c) moves forward at a rate less than one cell per time step, while
%%%% returning to the same shape after some period.

N = 10;
C = ones(N);
C(9, 7) = 0; C(7, 7) = 0; C(7, 9) = 0;
C(8, 7) = 2; C(8, 6) = 2; C(6, 8) = 2;
% firing_brain(N, 5, 1, 10, C);