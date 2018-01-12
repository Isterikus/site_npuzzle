#include "main.h"

int		*left_range;
int		*right_range;
int		*top_range;
int		*bottom_range;
int		*database;
int		n;
int		size;

void	set_range()
{
	int		i;

	left_range = (int *)malloc(sizeof(int) * n);
	right_range = (int *)malloc(sizeof(int) * n);
	top_range = (int *)malloc(sizeof(int) * n);
	bottom_range = (int *)malloc(sizeof(int) * n);
	i = 0;
	while (i < n)
	{
		left_range[i] = i * n;
		right_range[i] = (i + 1) * n - 1;
		top_range[i] = i;
		bottom_range[i] = size - i - 1;
		i++;
	}
}

int		abs(int x)
{
	if (x < 0)
		return -x;
	else
		return x;
}

int		getH(int *field)
{
	return getManhattan(field);// + getLinearConflictMine(field);
}

int		getManhattan(int *field)
{
	int		i;
	int		j;
	int		ret;
	int		pos;
	int		pl_i;
	int		pl_j;

	ret = 0;
	i = 0;
	while (i < n)
	{
		j = 0;
		while (j < n)
		{
			pos = i * n + j;
			if (field[pos] == 0) {
				pl_i = n - 1;
				pl_j = n - 1;
			} else if (field[pos] % n == 0) {
				pl_i = field[pos] / n - 1;
				pl_j = n - 1;
			} else {
				pl_i = field[pos] / n;
				pl_j = field[pos] % n - 1;
			}
			ret += abs(i - pl_i) + abs(j - pl_j);
			j++;
		}
		i++;
	}
	return ret;
}

int		getLinearConflictMine(int *field)
{
	int		ret;
	int		i;
	int		j;
	int		k;

	ret = 0;
	i = 0;
	while (i < n) {
		j = 0;
		while (j < n) {
			k = i;
			while (k < n) {
				if (field[i * n + j] > field[k * n + j])
					ret += 2;
				k++;
			}
			k = j;
			while (k < n) {
				if (field[i * n + j] > field[i * n + k])
					ret += 2;
				k++;
			}
			j++;
		}
		i++;
	}
	return ret;
}

int		compare_array(int *field1, int *field2)
{
	int		i;

	i = 0;
	while (i < size)
	{
		if (field1[i] != field2[i])
			return 0;
		i++;
	}
	return 1;
}

int		ansver(int *field)
{
	int		i;

	i = 0;
	while (i < size - 1)
	{
		if (field[i] != i + 1)
			return 0;
		i++;
	}
	if (field[size - 1] != 0)
		return 0;
	return 1;
}

void	print_way(t_state *node)
{
	int		i;
	int		j;
	int		len = 0;

	while (node != NULL)
	{
		i = 0;
		while (i < n)
		{
			j = 0;
			while (j < n)
			{
				printf("%d ", (*node).field[i * n + j]);
				j++;
			}
			i++;
			printf("\n");
		}
		printf("----------------------------------\n");
		node = node->parent;
		len++;
	}
	printf("LEN = %d\n", len);
}

int		elemInArray(int elem, int arr_num)
{
	int		i;
	int		*arr;

	i = 0;
	if (arr_num == 1)
		arr = left_range;
	else if (arr_num == 2)
		arr = right_range;
	else if (arr_num == 3)
		arr = top_range;
	else
		arr = bottom_range;
	while (i < n) {
		if (arr[i++] == elem) {
			// printf("RETURN 1[%d][%d]\n", arr[i - 1], elem);
			return 1;
		}
	}
	return 0;
}

int		*copyField(int *field)
{
	int		*new_field;
	int		i;

	new_field = (int *)malloc(sizeof(int) * size);
	i = 0;
	while (i < size) {
		new_field[i] = field[i];
		i++;
	}
	return new_field;
}

int		*swap(int *field, int num1, int num2)
{
	field[num2] += field[num1];
	field[num1] = field[num2] - field[num1];
	field[num2] = field[num2] - field[num1];
	return field;
}

t_state	*find_neighbor(int num, int *field)
{
	int		now;
	int		i;
	t_state	*state;

	i = 0;
	state = NULL;
	while (i < size) {
		if (field[i] == 0)
			now = i;
		i++;
	}
	if (num == 1 && !elemInArray(now, 1)) {
		state = (t_state *)malloc(sizeof(t_state));
		state->field = swap(copyField(field), now, now - 1);
	}
	else if (num == 2 && !elemInArray(now, 2)) {
		state = (t_state *)malloc(sizeof(t_state));
		state->field = swap(copyField(field), now, now + 1);
	}
	else if (num == 3 && !elemInArray(now, 3)) {
		state = (t_state *)malloc(sizeof(t_state));
		state->field = swap(copyField(field), now, now - n);
	}
	else if (num == 4 && !elemInArray(now, 4)) {
		state = (t_state *)malloc(sizeof(t_state));
		state->field = swap(copyField(field), now, now + n);
	}
	i = 0;
	return state;
}

int		search(t_state *node, int g, int bound)
{
	int		f;
	int		i;
	int		t;
	t_state	*succ;

	f = g + getH(node->field);
	if (f > bound)
		return 0;
	if (ansver(node->field)) {
		// print_way(node);
		return 1;
	}
	i = 1;
	while (i <= 4)
	{
		succ = find_neighbor(i, node->field);
		if (succ == NULL) {
			i++;
			continue;
		}
		if (node->parent && compare_array(node->parent->field, succ->field)) {
			free(succ->field);
			free(succ);
			i++;
			continue;
		}
		succ->parent = node;
		if (g + 1 + getH(succ->field) <= bound)
		{
			t = search(succ, g + 1, bound);
			if (t)
				return 1;
		}
		i++;
	}
	return 0;
}

void	idaStar(int *initial_field)
{
	t_state	*initial;
	int		bound;
	int		t;

	initial = (t_state *)malloc(sizeof(t_state));
	initial->g = 0;
	initial->field = initial_field;
	initial->parent = NULL;
	bound = getH(initial->field);
	while (1)
	{
		t = search(initial, 0, bound);
		if (t)
			break;
		bound += 2;
	}
	free(initial);
}

t_state	*pop(t_sts **start)
{
	t_state	*ret;

	ret = (*start)->state;
	(*start) = (*start)->next;
	return ret;
}

t_state	*min(t_sts	**start)
{
	t_sts	*prev;
	t_sts	*temp;
	t_sts	*go;
	t_sts	*prev_go;
	t_state	*ret;
	int		min;

	prev = NULL;
	prev_go = NULL;
	go = *start;
	temp = *start;
	min = temp->state->h;
	while (temp) {
		if (temp->state->h < min) {
			min = temp->state->h;
			prev_go = prev;
			go = temp;
		}
		prev = temp;
		temp = temp->next;
	}
	ret = go->state;
	if (prev_go == NULL) {
		free(*start);
		*start = go->next;
	} else {
		prev_go->next = go->next;
		free(go);
	}
	return ret;
}

void	add_node(t_sts *list, t_state *state)
{
	if (list->state != NULL) {
		while (list->next != NULL) {
			list = list->next;
		}
		list->next = (t_sts *)malloc(sizeof(t_sts));
		list->next->state = state;
		list->next->next = NULL;
	} else {
		list->state = state;
	}
}

int		not_in(t_sts *list, t_state *check)
{
	while (list != NULL) {
		if (compare_array(list->state->field, check->field)) {
			return 0;
		}
		list = list->next;
	}
	return 1;
}

void	append(t_sts **list, t_state *app)
{
	t_sts	*new;

	new = (t_sts *)malloc(sizeof(t_sts));
	new->state = app;
	new->next = (*list);
	(*list) = new;
}

void	aStar(int *initial_field)
{
	t_state	*initial;
	t_state	*current;
	t_sts	*closed;
	t_sts	*opened;
	t_state	*succ;
	int		i;

	initial = (t_state *)malloc(sizeof(t_state));
	initial->g = 0;
	initial->field = initial_field;
	initial->parent = NULL;
	initial->h = getH(initial->field);
	opened = (t_sts *)malloc(sizeof(t_sts));
	closed = (t_sts *)malloc(sizeof(t_sts));
	opened->state = initial;
	closed->state = NULL;
	opened->next = NULL;
	closed->next = NULL;
	while(opened) {
		current = min(&opened);
		if (ansver(current->field)) {
			print_way(current);
			free(initial);
			return;
		}
		add_node(closed, current);
		i = 1;
		while (i < 5) {
			succ = find_neighbor(i, current->field);
			if (succ == NULL) {
				i++;
				continue;
			}
			if (current->parent && compare_array(current->parent->field, succ->field)) {
				free(succ->field);
				free(succ);
				i++;
				continue;
			}
			if (not_in(closed, succ)) {
				succ->parent = current;
				succ->h = current->g + 1 + getH(succ->field);
				if (not_in(opened, succ)) {
					append(&opened, succ);
				}
			}
			i++;
		}
	}
	free(initial);
}

void	python(int sz, char *field, char *algo, char *heuristics)
{
	heuristics = NULL;








	int		*initial_field;
	int		i;
	int		j;

	n = sz;
	size = n * n;
	initial_field = (int *)malloc(sizeof(int) * size);
	i = 0;
	j = 0;
	while (field[i])
	{
		initial_field[j] = 0;
		while (field[i] && field[i] != ',')
			initial_field[j] = initial_field[j] * 10 + field[i++] - 48;
		if (field[i])
			i++;
		j++;
	}
	set_range();
	if (ft_strcmp("idaStar", algo)) {
		idaStar(initial_field);
	} else if (ft_strcmp("aStar", algo)) {
		aStar(initial_field);
	}
	free(left_range);
	free(right_range);
	free(top_range);
	free(bottom_range);
}

int		main(int argc, char const *argv[])
{
	int		*initial_field;
	int		i;
	int		j;

	if (argc != 3)
		return 0;
	printf("START C\n");
	n = atoi(argv[1]);
	size = n * n;
	initial_field = (int *)malloc(sizeof(int) * size);
	i = 0;
	j = 0;
	while (argv[2][i])
	{
		initial_field[j] = 0;
		while (argv[2][i] && argv[2][i] != ',')
			initial_field[j] = initial_field[j] * 10 + argv[2][i++] - 48;
		if (argv[2][i])
			i++;
		j++;
	}
	set_range();
	aStar(initial_field);
	free(left_range);
	free(right_range);
	free(top_range);
	free(bottom_range);
	return 0;
}
