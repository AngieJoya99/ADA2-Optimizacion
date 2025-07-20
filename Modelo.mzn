%Lectura de datos:
int: n;
int: m;
array[1..m] of int: p;
array[1..m] of float: ext;
array[1..m] of float: ce;
array[1..m,1..m] of float: c;
float: ct;
int: maxM;

%Variables:
array[1..m,1..m] of var 0..n: x;
array [1..m] of var 0..n: sol;
var float: extremismo;

%Restricciones:
constraint forall(i in 1..m, j in 1..m)(x[i,j] >= 0);
constraint sum(i in 1..m)(sum(j in 1..m)( (j - i)* x[i,j] )) <= maxM;
constraint forall(i in 1..m)(sum(j in 1..m)(x[i,j]) <= p[i]);
constraint forall(i in 1..m, j in 1..m where i==j)( x[i,j] = 0);
constraint forall(i in 1..m)(
  sol[i]=p[i] - sum(k in 1..i, j in 1..m)(x[k,j]) + sum(k in 1..m, j in 1..i)(x[k,j])
);
var float: total_cost;

constraint
  total_cost = sum(i in 1..m, j in 1..m where i != j)(
    let {
      float: base = c[i,j] * (1 + p[i]/int2float(n)),
      bool: arrival_empty = p[j] == 0
    } in
      x[i,j] * (base + (if arrival_empty then ce[j] else 0.0 endif))
  );

constraint total_cost <= ct;

%constraint extremismo = sum(i in 1..m) (p[i] - sum(j in 1..m where i!=j)(x[i,j] )*ext[i] );
constraint extremismo = sum(i in 1..m) (sol[i] *ext[i]);

%Objetivo
solve minimize extremismo;