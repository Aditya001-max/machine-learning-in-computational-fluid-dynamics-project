// nozzle.geo — CORRECTED
h = 0.08; // mesh size

// Define 2D cross-section points
Point(1) = {0, 0, 0, h};
Point(2) = {0, 0.25, 0, h};
Point(3) = {-0.2, 0.25, 0, h};
Point(4) = {-0.2, 0.5, 0, h};
Point(5) = {1.75, 0.5, 0, h};
Point(6) = {1.75, 0, 0, h};
Point(7) = {2.55, 0.05, 0, h};
Point(8) = {2.55, 0.45, 0, h};


//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 5};
//+
Line(5) = {5, 8};
//+
Line(6) = {8, 7};
//+
Line(7) = {7, 6};
//+
Line(8) = {6, 1};
//+
Curve Loop(1) = {4, 5, 6, 7, 8, 1, 2, 3};
//+
Plane Surface(1) = {1};
//+
Extrude {0, 0, 0.25} {
  Surface{1}; 
}
//+
Physical Surface("inlet", 51) = {49};
//+
Physical Surface("outlet", 52) = {29};
//+
Physical Surface("top", 53) = {21, 25};
//+
Physical Surface("bottom", 54) = {37, 33, 41, 45};
//+
Physical Surface("front_back", 55) = {1, 50};
//+
Physical Volume("fluid", 56) = {1};
