SetFactory("OpenCASCADE");
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {15, 0, 0, 1.0};
//+
Point(3) = {15, 10, 0, 1.0};
//+
Point(4) = {0, 10, 0, 1.0};
//+
Point(5) = {2, 5.0, 0, 0.1};
Point(6) = {2, 4.5, 0, 0.1};
Point(7) = {2.5, 5.0, 0, 0.1};
Point(8) = {2, 5.5, 0, 0.1};
Point(9) = {1.5, 5.0, 0, 0.1};
Circle(7) = {6, 5, 7};
Circle(8) = {7, 5, 8};
Circle(9) = {8, 5, 9};
Circle(10) = {9, 5, 6};
Line(3) = {1, 2};
//+
Line(4) = {2, 3};
//+
Line(5) = {3, 4};
//+
Line(6) = {4, 1};
//+
Curve Loop(2) = {5, 6, 3, 4};
//+
Curve Loop(3) = {9, 10, 7, 8};
//+
Plane Surface(2) = {2, 3};
//+
Extrude {0, 0, 1} {
  Surface{2}; 
  Layers{1};
  Recombine;
}
//+
Physical Surface("In", 27) = {4};
//+
Physical Surface("Out", 28) = {6};
//+
Physical Surface("Top", 29) = {3};
//+
Physical Surface("Bottom", 30) = {5};
//+
Physical Surface("FrontBack", 31) = {11, 2};
//+
Physical Surface("circle", 32) = {7, 8, 9, 10};
//+
Physical Volume("Internal", 33) = {1};
