% "Combined state and least squares parameter estimation algorithms for dynamic systems"

%����������������������������������������������������������������������������������������������������������������������������������������������*
%Filename: SS_ParamState_Ao_RLS_ex1.m *
% for observer canonical state space systems *
% x (t + 1)=Ax (t)+ bu (t) *
% y (t)=cx (t)+v (t) *
% Parameter and state estiamtion algorithm *
% u (t): The model input: an uncorrelated stochastic signal sequence *
% with zero mean and unit variance,
% v (t): The disturbance: an uncorrelated white noise sequence *
% with zero mean and variance sigma^2,
% y (t): The model output,
% *
% The noise variance sigma ^2 = 1.00 ^2 and 2.00^2 *
% The forgetting factor k =FF=1 *
% Date: 2012/11/18 Sunday 23:30 *
%-------------------------------------------------
% Copyright 2008-
% Feng Ding (Ding Feng, F. Ding, Ding F.)
% School of Internet of Things Engineering
% Jiangnan University, Wuxi, PR China, 214122
% Email: fding@jiangnan.edu.cn
% www.fding.org www.fding.org/df2012
%
% Revision Date: xxx/xx/xx hh:mm:ss By whom
%------------------------------
clear all;
clc;
format short g;
% clf
fprintf ('\n The parameter and state estimation algorithm \n')
FF=1; % The forgetting factor FF = k =1
sigma =0.5; % The noise variance sigma ^2 = 1.0^2 and 2.0^2
PlotLength = 5000;
length1=PlotLength + 100;
n = 2; % The orders
A=[ 0.8,1;-0.4,0];
b=[1.68, 2.32]';
c=[1, 0];
d = 0;
ss1 = ss(A,b,c,d);
par0=[-A(:,1); b];
n1 = length(par0);
p0=1e6;
P=eye(n1)*p0;
r =1;
par1 = ones (n1,1)/p0;
P2 = eye(n)*1; % The covariance matrix of the Kalman filter
%�CCompute the noise-to-signal ratio

% a=[1, -A(:,1)'];
% sy = f_integral (a,b); sv = 1;
% delta_ns = sqrt (sv/sy)*100*sigma;
% [sy,sv,delta_ns]

%����Generate the input�Coutput data
rand('state',2);
randn('state',2);
u=(rand(length1,1)-0.5)*sqrt(12);
v = randn(length1,1)*sigma;


x1 = ones(n1,1)/p0;
x2 = x1;
y = x1;
for t = n:length1
    x=[x1(t), x2(t)]';
    x1(t + 1)=A(1,:)*x + b(1)*u(t);
    x2(t + 1)=A(2,:)*x + b(2)*u(t);
    y(t)=c*x + v(t);
end
%����Compute the parameter estimates
hx1 = zeros(n1,1);
hx2 = hx1;
jj = 0;
j1 = 0;
for t =n1:length1
    jj = jj + 1;
    varphi=[-hx1(t-1:-1:t-n);u(t-1:-1:t-n)];
    
    L=P*varphi/(FF + varphi'*P*varphi);
    P=(P-L*varphi'*P)/FF;
    par1 = par1 + L*(y(t)-varphi'*par1);
    
    A1=[-par1(1:n), [1;0]];
    b1 = par1(n + 1:n1);
    
    L2 = A1*P2*c'/(1 + c*P2*c');
    P2 = A1*P2*A1'-L2*c*P2*A1';
    %     P2 = A1'*P2*A1'-L2*c*P2*A1';
    hx=[hx1(t); hx2(t)];
    hx1(t + 1)=A1(1,:)*hx + b1(1)*u(t) +L2(1)*(y(t)-c*hx);
    hx2(t + 1)=A1(2,:)*hx + b1(2)*u (t)+L2(2)*(y (t)-c*hx);
    delta = norm(par1-par0)/norm(par0);
    ls(jj,:)=[jj,par1',delta];
    if (jj==100)|(jj==200)|(jj==500)|mod (jj,1000)==0
        j1 = j1 + 1;
        ls100(j1,:)=[jj, par1', delta*100];
    end
    if jj==PlotLength
        break
    end
end
ls100(j1 + 1,:)=[0, par0', 0];
% fprintf ('\n($\\sigma^2=%5.2f^2$,$\\delta_{\\ns}=%6.2f%s)\n',sigma,delta_ns,'\%')
% fprintf ('\n%s \n',' $t$&$a_1$&$a_2$&$b_1$&$b_2$&$\delta\(\%) \\$ \\\\hline');
% fprintf ('%5d & %10.5f & %10.5f & %10.5f & %10.5f & %10.5f \\\\\',ls100');
figure(1);
k=(17:PlotLength-1)';
plot(ls(k,1),ls(k,n1 + 2));
axis([0, PlotLength, 0, 0.51]);
xlabel('t');
ylabel('\delta');

figure(2);
k=(20:PlotLength-1)';
plot(k,ls(k,2),'k',k,ls(k,3),'b',k,ls(k,4),'k',k,ls(k,5),'b');
xlabel('t');
ylabel('Parameter estimates');
% axis([0, PlotLength, 1.1, 3.6]);
k = 2500;
text(k,ls(k,2)+0.25,'a_1');
text(k,ls(k,3)+0.25,'a_2')
text(k,ls(k,4)+0.25,'b_1');
text(k,ls(k,5)+0.25,'b_2')
if sigma==1.0
    data1=[ls(:,1), ls(:,n1 + 2)];
    save data1 data1
else % sigma==2.0
    load data1
    z0=[data1,ls(:,n1 + 2)];
    figure(3);
    k=(17:2:PlotLength-1)';
    jk = z0(k,1);
    plot(jk,z0(k,2),'k',jk,z0(k,3),'b')
    axis([0, PlotLength, 0, 0.72]);
    xlabel('t');
    ylabel('\delta');
    line([800,1400],[z0(800,2),0.3])
    text(1400,0.3 + 0.03,'\it \sigma^2 = 1.00 ^2')
    line([2000,2800],[z0(2000,3),0.3])
    text (2800,0.3 + 0.03,'\sigma^2 = 2.00^2')
end