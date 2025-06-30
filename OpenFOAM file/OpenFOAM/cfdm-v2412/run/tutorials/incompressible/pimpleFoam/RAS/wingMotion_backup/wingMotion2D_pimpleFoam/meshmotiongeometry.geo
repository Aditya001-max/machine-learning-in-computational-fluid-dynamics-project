// Points
Point(1) = {-1, -1, 0, 0.1};
Point(2) = {1, -1, 0, 0.1};
Point(3) = {1, 1, 0, 0.1};
Point(4) = {-1, 1, 0, 0.1};
Point(5) = {0, 0, 0, 0.1};
Point(6) = {0.3, 0, 0, 0.1};
Point(7) = {0, 0.3, 0, 0.1};
Point(8) = {0, -0.3, 0, 0.1};
Point(9) = {-0.3, 0, 0, 0.1};

// Outer square lines
Line(1) = {4, 3};
Line(2) = {3, 2};
Line(3) = {2, 1};
Line(4) = {1, 4};

// Inner circle arcs (clockwise)
Circle(5) = {7, 5, 6};
Circle(6) = {6, 5, 8};
Circle(7) = {8, 5, 9};
Circle(8) = {9, 5, 7};

// Curve loops
Curve Loop(1) = {5, 6, 7, 8}; // Inner hole
Curve Loop(2) = {4, 1, 2, 3}; // Outer square

// Create planar surface with circular hole
Plane Surface(1) = {1, 2};

// Extrude 2D surface to create 3D geometry
Extrude {0, 0, 0.1} {
  Surface{1}; Layers{1}; Recombine;
}

// Create physical surfaces
Physical Surface("inlet") = {49};      // adjust after mesh export if needed
Physical Surface("outlet") = {41};
Physical Surface("top") = {45};
Physical Surface("bottom") = {37};
Physical Surface("front_back") = {50, 1};
Physical Surface("cylinder") = {21, 25, 29, 33};

// ✅ This is **crucial**:
Physical Volume("fluid") = {1};        // volume ID will be 1, not 2

