first(X, [X | _]).

main :-
    S1="hanoi(",
    S3=")",
    write('Welcome to the Hanoi-as-a-Service cloud platform!'),nl,write('How many disks does your tower have?'), nl,
    read_line_to_codes(user_input, F),
    append(S1, F, S2),
    append(S2, S3, S4),
    string_to_atom(S4, PWN),
    read_term_from_atom(PWN, T, []),
    T,
    halt(0).

hanoi(N) :-
    N < 15,
    dohanoi(N, a, b, c). % Move the tower from peg a to peg b

hanoi(N) :-
    N >= 15,
    write('Hey, this problem is too big for my poor mind...'), nl.

dohanoi(0, _, _, _)	:- !.
dohanoi(N, A, B, C)	:- !,
    N1 is N-1,
    dohanoi(N1, A, C, B), % move the N-1 top-most from A to C
    moveit(A, B),         % move the last one
    dohanoi(N1, C, B, A). % move the ones in C to B

moveit(F, T) :- print('* Move top disk from '), print(F), print(' to '), print(T), nl.

