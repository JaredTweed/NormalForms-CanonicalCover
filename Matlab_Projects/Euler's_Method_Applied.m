% MACM 316 - Week 12
% Euler's method demo
% Description: Applies Euler's method
% File name: Euler1.m

clear;clf;

% IVP parameters
a=0;
b=200;
h=0.0005;
N=(b-a)/h;

q1 = zeros(N+1, 1); % distance
q2 = zeros(N+1, 1);
p1 = zeros(N+1, 1); % velocity
p2 = zeros(N+1, 1);
A = zeros(N+1, 1);
H = zeros(N+1, 1);
q1_3 = zeros(N+1, 1);
q2_3 = zeros(N+1, 1);
p1_3 = zeros(N+1, 1); 
p2_3 = zeros(N+1, 1);
A_3 = zeros(N+1, 1);
H_3 = zeros(N+1, 1);

% Initial values
e = 0.6;
q1(1) = 1-e;
q2(1) = 0;
p1(1) = 0;
p2(1) = sqrt((1+e)/(1-e));
q1_3(1) = 1-e;
q2_3(1) = 0;
p1_3(1) = 0;
p2_3(1) = sqrt((1+e)/(1-e));

% Euler steps
for i=1:N+1
    % Part 1
    
    % Find q1 and q2 for i+1
    q1(i+1) = q1(i) + h*p1(i);
    q2(i+1) = q2(i) + h*p2(i);

    % Find p1 and p2 for i+1
    p1(i+1) = p1(i) + ((-q1(i))/((q1(i)^2 + q2(i)^2)^(3/2)))*h;
    p2(i+1) = p2(i) + ((-q2(i))/((q1(i)^2 + q2(i)^2)^(3/2)))*h;


    % Part 2
    A(i) = q1(i)*p2(i) - q2(i)*p1(i);
    H(i) = 0.5*(p1(i)^2 + p2(i)^2) - (1/sqrt(q1(i)^2 + q2(i)^2));


    % Part 3

    % Find q1 and q2 for i+1
    q1_3(i+1) = q1_3(i) + h*p1_3(i);
    q2_3(i+1) = q2_3(i) + h*p2_3(i);

    % Find p1 and p2 for i+1
    p1_3(i+1) = p1_3(i) + ((-q1_3(i+1))/((q1_3(i+1)^2 + q2_3(i+1)^2)^(3/2)))*h;
    p2_3(i+1) = p2_3(i) + ((-q2_3(i+1))/((q1_3(i+1)^2 + q2_3(i+1)^2)^(3/2)))*h;

    A_3(i) = q1_3(i)*p2_3(i) - q2_3(i)*p1_3(i);
    H_3(i) = 0.5*(p1_3(i)^2 + p2_3(i)^2) - (1/sqrt(q1_3(i)^2 + q2_3(i)^2));

end

% Plot Part 1
figure(1);
subplot(3,2,1);
hold on
plot(q1,q2,'r')
pbaspect([3,1,1]); % aspect ratio

title('Forward Euler''s Method Part 1 (Figure 1)','fontsize',10)
xlabel('q1-axis','fontsize',12)
ylabel('q2-axis','fontsize',12)
%legend({'y(t)','Euler'},'fontsize',14,'Location','southeast')

% Plot Part 2
% figure(2);
subplot(3,2,3);
hold on
plot(a:h:b,A,'r')
pbaspect([3,1,1]);

title('Forward Euler''s Method Part 2 (Figure 2)','fontsize',10)
xlabel('Time','fontsize',12)
ylabel('Angular Momentum','fontsize',10)

% figure(3);
subplot(3,2,5);
hold on
plot(a:h:b,H,'r')
pbaspect([3,1,1]);

title('Forward Euler''s Method Part 2 (Figure 3)','fontsize',10)
xlabel('Time','fontsize',12)
ylabel('The Hamiltonian','fontsize',12)

% Plot Part 3
% figure(4);
subplot(3,2,2);
hold on
plot(q1_3,q2_3,'r')
pbaspect([3,1,1]);

title('Symplectic Euler''s Method Part 3 (Figure 4)','fontsize',10)
xlabel('q1-axis','fontsize',12)
ylabel('q2-axis','fontsize',12)
%legend({'y(t)','Euler'},'fontsize',14,'Location','southeast')


% figure(5);
subplot(3,2,4);
hold on
plot(a:h:b, A_3,'r')
pbaspect([3,2,1]);

title('Symplectic Euler''s Method Part 3 (Figure 5)','fontsize',10)
xlabel('Time','fontsize',12)
ylabel('Angular Momentum','fontsize',10)

% figure(6);
subplot(3,2,6);
hold on
plot(a:h:b, H_3,'r')
pbaspect([3,1,1]);

title('Symplectic Euler''s Method Part 3 (Figure 6)','fontsize',10)
xlabel('Time','fontsize',12)
ylabel('The Hamiltonian','fontsize',12)
