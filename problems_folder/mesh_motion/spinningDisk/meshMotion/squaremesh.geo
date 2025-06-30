Nx1 = 41; Rx1 = 1.00;
Nx2 = 81; Rx2 = 1.00;
Ny1 = 41; Ry1 = 1.00;
Ni  = 61; Ri  = 0.93;
Nc  = 41; Rc  = 1.00;

Point(1) = {-7, -7, 0, 1.0};
Point(2) = {7, -7, 0, 1.0};

Point(3) = {-0.353553391, -0.353553391, 0, 1.0};
Point(4) = {0.353553391, -0.353553391, 0, 1.0};
Point(5) = {-0.353553391, 0.353553391, 0, 1.0};
Point(6) = {0.353553391, 0.353553391, 0, 1.0};

Point(7) = {-7, 7, 0, 1.0};
Point(8) = {7, 7, 0, 1.0};
Point(9) = {0, 0, 0, 1.0};


//+
Line(1) = {1, 2};Transfinite Line {1}  = Nx1 Using Progression Rx1;
//+
Line(2) = {7, 8};Transfinite Line {2}  = Nx1 Using Progression Rx1;
//+
Line(3) = {1, 7};Transfinite Line {3}  = Ny1 Using Bump Ry1;
//+
Line(4) = {2, 8};Transfinite Line {4}  = Ny1 Using Bump Ry1;
//+
Line(5) = {1, 3};Transfinite Line {5}  = Ni Using Progression Ri;
//+
Line(6) = {2, 4};Transfinite Line {6}  = Ni Using Progression Ri;
//+
Line(7) = {8, 6};Transfinite Line {7}  = Ni Using Progression Ri;
//+
Line(8) = {7, 5};Transfinite Line {8}  = Ni Using Progression Ri;

//+
Circle(9) = {3, 9, 4};Transfinite Line {9} = Nc Using Progression Rc;
//+
Circle(10) = {4, 9, 6};Transfinite Line {10} = Nc Using Progression Rc;
//+
Circle(11) = {6, 9, 5};Transfinite Line {11} = Nc Using Progression Rc;
//+
Circle(12) = {5, 9, 3};Transfinite Line {12} = Nc Using Progression Rc;


//+
Curve Loop(1) = {1, 6, -9, -5};
//+
Plane Surface(1) = {1};
//+
Curve Loop(2) = {6, 10, -7, -4};
//+
Plane Surface(2) = {2};
//+
Curve Loop(3) = {7, 11, -8, 2};
//+
Plane Surface(3) = {3};
//+
Curve Loop(4) = {8, 12, -5, 3};
//+
Plane Surface(4) = {4};

Transfinite Surface {1};
Transfinite Surface {2};
Transfinite Surface {3};
Transfinite Surface {4};





//+
Extrude {0, 0, 1} {
  Surface{1,2,3,4};
  Layers{1};
  Recombine;
}
//+
Physical Surface("inlet", 101) = {99};
//+
Physical Surface("outlet", 102) = {55};
//+
Physical Surface("walls", 103) = {77, 21};
//+
Physical Surface("frontAndBack", 104) = {56, 78, 100, 34, 1, 4, 2, 3};
//+
Physical Surface("cylinder", 105) = {69, 91, 29, 47};
//+
Physical Volume("volume", 106) = {1, 2, 3, 4};
