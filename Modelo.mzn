% Use this editor as a MiniZinc scratch book
%Lectura de datos:
int: n; % Numero total de personas
int: m; % Numero de opiniones posibles
array[1..m] of int: p; % Numero de personas que tienen como opinion inicial la opinion i
array[1..m] of float: ext; % Valor de extermismo de cada opinion
array[1..m] of float: ce; % Costo extra de mover una persona a la posicion i si dicha posicion estaba inicialmente sin personas
array[1..m,1..m] of float: c; % Esfuerzo de mover una persona de la opinion i a la opinion j
float: ct; % Costo total maximo permitido
int: maxM; % Numero maximo de movimientos permitidos

int: maxp = max(p);

%Variables:
array[1..m,1..m] of var 0..maxp: x; % Numero de personas que cambian su opinion de la i a la j
var float: extremismo; % variable objetivo a minimizar
array [1..m] of var 0..n: sol; % Solucion final
var float: total_cost; % Costo total

%Restricciones:

% No negatividad
constraint forall(i in 1..m, j in 1..m)(x[i,j] >= 0);

% La cantidad de movimientos tiene que ser menor o igual a la permitida
constraint (sum (i in 1..m, j in 1..m where x[i,j] != 0)( abs(j-i) * x[i,j])) <= maxM;

% El numero de personas que se mueven de una opinion a otra no puede ser mayor que el numero de personas inicial
constraint forall(i in 1..m)(sum(j in 1..m)(x[i,j]) <= p[i]);

% Es la misma opinion, por lo tanto, la cantidad de personas que cambian de opinion es 0
constraint forall(i in 1..m, j in 1..m where i==j)( x[i,j] = 0);

% Obtiene la solucion final
constraint forall(i in 1..m)(
  sol[i] = p[i] % Valor inicial
          - sum(j in 1..m)( x[i,j] )   % Cantidad de personas que cambian de opinion i
          + sum(k in 1..m)( x[k,i] )   % Cantidad de personas que cambian a la opinion i
);

% Calculo del costo total
constraint
  total_cost = sum(i in 1..m, j in 1..m where i != j)(
    let {
      float: base = c[i,j] * (1 + p[i]/int2float(n)),
      bool: arrival_empty = p[j] == 0
    } in
      (x[i,j] * base) + (if arrival_empty then ce[j] * x[i,j] else 0.0 endif)
);

% El costo total debe de ser menor al permitido
constraint total_cost <= ct;

% Calculo del extremismo resultante (valor solucion)
constraint extremismo = sum(i in 1..m) (sol[i] * ext[i]);

% No negatividad
constraint total_cost >= 0;
constraint extremismo >= 0;

% Restricciones extras
constraint sum(i in 1..m)(sol[i]) == n;
constraint extremismo <= sum(i in 1..m)(p[i]*ext[i]); 
constraint forall(i in 1..m where p[i] = 0)(
  sum(j in 1..m)(x[i,j]) = 0
);

constraint forall(i in 1..m, j in 1..m where ext[j] >= ext[i])(
  x[i,j] = 0
);
  

%Objetivo
solve minimize extremismo;