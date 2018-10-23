#ifndef COREWAR_H
# define COREWAR_H

#include <sys/time.h>
#include <stdio.h>
#include <limits.h>
#include <string.h>
#include <stdint.h>
#include "libft/printf_functions/includes/header.h"

#define BUFF_SIZE 1000000

typedef struct		s_state
{
	int				*field;
	int				h;
	int				g;
	struct s_state	*parent;
}					t_state;

typedef struct		s_sts
{
	t_state			*state;
	struct s_sts	*next;
}					t_sts;

typedef struct		s_db
{
	// char			field[22];
	int				val;
	struct s_db		**next;
}					t_db;

typedef struct		s_realPos
{
	int				i;
	int				j;
}					t_realPos;

void	set_range();
int		abs(int x);
int		getH(int *field);
int		getManhattan(int *field);
int		getLinearConflict(int *field);
int		getLinearConflictMine(int *field);
int		getPatternDatabaseMine(int *field);
int		getPatternDatabase(int *field);
int		compare_array(int *field1, int *field2);
int		ansver(int *field);
void	print_way(t_state *node);
int		elemInArray(int elem, int arr_num);
int		*copyField(int *field);
int		*swap(int *field, int num1, int num2);
t_state	*find_neighbor(int num, int *field);
int		search(t_state *node, int g, int bound);
void	solve(int *initial_field);

#endif
