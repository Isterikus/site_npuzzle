

all:
	gcc -Wall -Wextra -Werror -O3 main.c libft/libftprintf.a

toPython:
	gcc -o adder.so -shared -fPIC main.c libft/libftprintf.a
	cp adder.so ../
