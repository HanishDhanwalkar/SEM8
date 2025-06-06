%DH parameters for the two-link manipulator
clear all 
clc

a1 = 1; d1 = 0; alpha1 = 0; offset1 = 0;
a2 = 1; d2 = 0; alpha2 = 0; offset2 = 0;


%setting up link parameters
L1 = Link('revolute','d', d1, 'a', a1, 'alpha', alpha1);
L1.m = 10;        
%Coordinates of center of mass in frame 1
L1.r = [-0.5; 0; 0]; 
%moment of inertial matrix in frame 1
L1.I = [0 0 0; 0 a1^2*L1.m/12 0; 0 0 a1^2*L1.m/12];
%Motor inertia Jm
L1.Jm = 0.1;
L1.B = 0;
%Gear Ratio for motor driving link 1
L1.G = 1;
L2.Tc = 0;
% 
L2 = Link('revolute','d', d2, 'a', a2, 'alpha', alpha2,'offset', offset2);


L2.m = 10;
%Coordinates of center of mass in frame 2
L2.r = [-0.5; 0; 0]; 
%moment of inertial matrix
L2.I = [0 0 0; 0 a2^2*L2.m/12 0; 0 0 a2^2*L2.m/12];
L2.Jm = 0.1;
L2.B = 0;
L2.G = 1;
L2.Tc = 0;
% %L2.nofriction();
% % 
%define the robot
bot = SerialLink([L1 L2], 'name', 'mybot');
%transformation between the base frame of the robot with the world frame
bot.base = [1 0 0 0;
              0 0 -1 0;
             0 1 0 1;
              0 0 0 1];

%desired goal position
%q_des = [-1 1];
% 
% 
% 
%T is the vector of time instants, Q is a matrix containing joint positions
%at times T(i) and QD is a matrix containing joint velocities at times T(i)
% Set @twolink_PD_Control to [] for zero torque
[T,Q,QD] = bot.fdyn(3, @twolink_PD_Control, [0.01,0.01], [0 0]);

%Animate and make a movie
%figure; bot.plot(Q);%,'movie','test.mp4'); 


%Kinetic Energy of the Manipulator
% for i = 1:length(QD)
%    qd_current = QD(i,:);
%    q_current = Q(i,:);
%    K(i) = 0.5*qd_current*bot.inertia(q_current)*qd_current';
% end

% %Potential Energy of the Manipulator
% for i = 1:length(Q)
%     q_current = Q(i,:);
%     [TMat,all] = bot.fkine(q_current);
%     Rc1 = all(1)*L1.r';
%     Rc2 = all(2)*L2.r';
%     P(i) = L1.m*9.81*Rc1(3) + L2.m*9.81*Rc2(3);
% end 


%hold on
%plot(T,Q(:,1));
%plot(T,Q(:,2));
grid on
%Plot total energy. 
%Energy should be conserved if no torque applied and friction = 0
%figure; plot(T,K+P)

%Calculate end-effector position
xp = cos(Q(:,1)) + cos(Q(:,1) + Q(:,2));
zp = 1 + sin(Q(:,1)) + sin(Q(:,1) + Q(:,2));

%plot joint angles and end-effector position
plot(T,Q(:,1)); hold on; plot(T,Q(:,2))
xlabel('time'); ylabel('Joint Position'); legend(['\theta_1';'\theta_2'])
figure; plot(xp,zp); xlabel('x'); ylabel('z');


%Function that defines controller behavior
function tau = twolink_PD_Control(robot, t, q, qd)

%Set point control
%Desired joint angles and rates
q1des = -pi/3;
q2des = pi/3;
qd1des = 0;
qd2des = 0;
qdd1des = 0;
qdd2des = 0;

%Desired end-effector position
xdes = [cos(q1des)+cos(q1des + q2des) 1+sin(q1des)+sin(q1des + q2des)];

%Desired joint angles and velocities; Trajectory tracking;
%Make sure both are consistent
%Comment for set point traking
%q1des = sin(15*t);
%q2des = cos(15*t);
%qd1des = 15*cos(15*t)
%qd2des = -15*sin(15*t)
%qdd1des = -15^2*sin(15*t)
%qdd2des = -15^2*cos(15*t)


%q = wrapToPi(q);

%Error and error-rate: joint-space control
e1 = q1des - q(1);
e2 = q2des - q(2);

e1d =  qd1des - qd(1);
e2d =  qd2des - qd(2);

%Gain for single dof unit mass system
omega = 2*pi*3;
Kpp = omega^2; Kvp = 2*omega;

%Multipliers (average inertia) for independent joint control
J1 = 2*10/3 + 1^2*0.1; %average value of d11 + G1^2*Jm1
J2 = 10/3 + 1^2*0.1;   %average value of d22 + G1^2*Jm1

%Scaling the gains with inertia for independent joint control
Kp1 = J1*Kpp; Kp2 = J2*Kpp;
Kv1 = J1*Kvp; Kv2 = J2*Kvp;

%Independent joint PD control torque computation
%No gravity compensation
tau(1) = J1*qdd1des + Kp1*e1 + Kv1*e1d;
tau(2) = J2*qdd2des + Kp2*e2 + Kv2*e2d;

%Independent joint PD control with gravity compensation
%Add gravity torque estimate to negate the effect of 
%gravitational forces

%tau(1) = Kp1*e1 - Kv1*qd(1);
%tau(2) = Kp2*e2 - Kv2*qd(2);
%tau = tau + robot.gravload(q);

%Nonlinear decoupling controller
%Cancel nonlinearities using your estimates
%Scale unit mass gains using Robot inertia matrix

%tau = robot.inertia(q)*([qdd1des; qdd2des]+Kpp*[e1; e2] + Kvp*[e1d;e2d]) + robot.coriolis(q, qd)*qd' + robot.gravload(q)';

%Task space PD control: Set point

%Current end-effector position
x = [cos(q(1))+cos(q(1) + q(2)) 1+sin(q(1))+sin(q(1)+q(2))];

%Computing Jacobian and end-effector velocity
Jfull = robot.jacob0(q);
J = [Jfull(1,:); Jfull(3,:)];
xd = J*qd';

%unit mass controller parameters  
omega = 3*2*pi;
Kpp = omega^2;
Kdp = 2*omega;
% 
%Task-space force for unit mass  
Fp = Kpp*(xdes - x)' + Kdp*(- xd);
% Scaling the unit mass force
F = 10*Fp;
% 
% Computing tau equivalent to -F acting on the end-effector
% and adding gravity torque estimate
%tau = J'*F +robot.gravload(q)';

tau = tau';
end
