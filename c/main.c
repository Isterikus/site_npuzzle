#include "main.h"
// gcc -o adder.so -shared -fPIC main.c libft/libftprintf.a

int			*left_range;
int			*right_range;
int			*top_range;
int			*bottom_range;
int			n;
int			size;
char		*heuristics;
t_db		*database1;
t_db		*database2;
t_db		*database3;
//int			patterns[3][5] = {{1, 2, 3, 5, 6}, {4, 7, 8, 11, 12}, {9, 10, 13, 14, 15}};
int			patterns[3][5] = {{1, 2, 3, 5, 6}, {4, 7, 8, 11, 12}, {9, 13, 14, 15, 0}};
t_realPos	*realPos;

int     *get_snake(int n)
{
    char    way;
    int     **arr;
    int     i;
    int     j;
    int     go_to;
    int     ch_go_to;
    int     cou_go_to;
    int     passed_way;
    int     count;
    int     *ret;

    way = 'r';
    arr = (int **)malloc(sizeof(int *) * n);
    ret = (int *)malloc(sizeof(int *) * n * n);
    i = 0;
    while (i < n)
    {
        arr[i] = (int *)malloc(sizeof(int) * n);
        i += 1;
    }
    i = 0;
    j = 0;
    go_to = n - 1;
    ch_go_to = 3;
    cou_go_to = 0;
    passed_way = 0;
    count = 1;
    while (count <= n ** 2)
    {
        arr[i][j] = count;
        if (count == n ** 2)
            arr[i][j] = 0;
        count += 1;
        if (way == 'r')
        {
            if (passed_way == go_to)
            {
                way = 'd';
                i += 1;
                cou_go_to += 1;
                passed_way = 1;
            } else
            {
                passed_way += 1;
                j += 1;
            }
        } else if (way == 'd')
        {
            if (passed_way == go_to)
            {
                way = 'l';
                j -= 1;
                cou_go_to += 1;
                passed_way = 1;
            } else
            {
                i += 1;
                passed_way += 1;
            }
        } else if (way == 'l')
        {
            if (passed_way == go_to)
            {
                way = 'u';
                i -= 1;
                cou_go_to += 1;
                passed_way = 1;
            } else
            {
                j -= 1;
                passed_way += 1;
            }
        } else if (way == 'u')
        {
            if (passed_way == go_to)
            {
                way = 'r';
                j += 1;
                cou_go_to += 1;
                passed_way = 1;
            } else
            {
                i -= 1;
                passed_way += 1;
            }
        }
        if (cou_go_to == ch_go_to)
        {
            cou_go_to = 0;
            go_to -= 1;
            if (ch_go_to == 3)
                ch_go_to = 2;
        }
    }
    i = 0;
    j = 0;
    count = 0;
    while (i < n)
    {
        while (j < n)
        {
            ret[count] = arr[i][j];
            count += 1;
            j += 1;
        }
        i += 1;
    }
    return ret;
}

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

	realPos = (t_realPos *)malloc(sizeof(t_realPos) * size);
	i = 1;
	while (i < size) {
		realPos[i].i = (i - 1) / n;
		realPos[i].j = (i - 1) % n;
		i++;
	}
}

t_db	*database(char *data, int len)
{
	int		i;
	int		j;
	t_db	*start;
	t_db	*temp;
	char	field[22];
	int		k;
	int		val;

	i = 0;
	start = (t_db *)malloc(sizeof(t_db));
	start->next = NULL;
	temp = start;
	while (i < len) {
		while (data[i] != '"') {
			i++;
		}
		i++;
		j = 0;
		while (data[i] != '"') {
			field[j++] = data[i++];
		}
		field[j] = '\0';
		i += 3;
		val = 0;
		while (data[i] != ',') {
			if (data[i] == '}') {
				return start;
			}
			val = val * 10 + data[i++] - 48;
		}
		k = 0;
		temp = start;
		while (k < j) {
			if (!temp->next) {
				temp->next = (t_db **)malloc(sizeof(t_db) * 10);
				for (int u = 0; u < 10; u++) {
					temp->next[u] = (t_db *)malloc(sizeof(t_db));
					temp->next[u]->next = NULL;
				}
			}
			// printf("[%c]\n", field[k]);
			temp = temp->next[field[k] - 48];
			k++;
		}
		// for (int u = 0; u < strlen(field); u++) {
		// 	temp->field[u] = field[u];
		// }
		// temp->field = strdup(field);
		temp->val = val;
		// temp->next = (t_db *)malloc(sizeof(t_db));
		// temp = temp->next;
		// temp->next = NULL;
	}
	return start;
}

void	readDatabases()
{
	char	*db;
	FILE	*fp;
	int		readed;
	int		iter;
	char	file[] = "databases/DATABASE_5_5_5-\0\0";

	int i = 1;
	while (i < 4) {
		db = (char *)malloc(sizeof(char) * 15189741);
		fp = fopen(ft_strcat(file, ft_itoa(i)), "r");
		file[25] = '\0';
		readed = 0;
		while (42) {
			iter = fread(db + readed, sizeof(char), 1000000, fp);
			readed += iter;
			if (iter < 1000000) {
				break;
			}
		}
		db[readed] = '\0';
		if (i == 1) {
			database1 = database(db, readed);
		} else if (i == 2) {
			database2 = database(db, readed);
		} else if (i == 3) {
			database3 = database(db, readed);
		}
		fclose(fp);
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

int		getManhattan(int *field)
{
	int		i;
	int		ret;

	ret = 0;
	i = 0;
	while (i < size) {
		if (field[i] != 0) {
			ret += abs(i / n - realPos[field[i]].i) + abs(i % n - realPos[field[i]].j);
		}
		i++;
	}
	return ret;
}

int		getLinearConflict(int *field)
{
	int		ret;
	int		i;
	int		j;
	int		max_i;
	int		max_j;
	int		val_i;
	int		val_j;

	ret = 0;
	i = 0;
	while (i < n) {
		j = 0;
		max_i = -1;
		max_j = -1;
		while (j < n) {
			val_i = field[i * n + j];
			val_j = field[j * n + i];
			if (val_i != 0 && (val_i - 1) / n == i) {
				if (val_i > max_i) {
					max_i = val_i;
				} else {
					ret += 2;
				}
			}
			if (val_j != 0 && val_j % n == i + 1) {
				if (val_j > max_j) {
					max_j = val_j;
				} else {
					ret += 2;
				}
			}
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

int		in_array(int *arr, int val)
{
	int		i;

	i = 0;
	while (i < 5) {
		if (arr[i++] == val) {
			return 1;
		}
	}
	return 0;
}

void	hash(char **str, int *field, int *pattern)
{
	int		i;
	int		j;

	i = 0;
	j = 0;
	while (i < size) {
		if (!in_array(pattern, field[i])) {
			(*str)[j] = '0';
		} else {
			if (field[i] > 9) {
				(*str)[j++] = '1';
				(*str)[j] = field[i] % 10 + 48;
			} else {
				(*str)[j] = field[i] % 10 + 48;
			}
		}
		j++;
		i++;
	}
	(*str)[j] = '\0';
}

int		find_db(t_db *db, char *hash)
{
	int		i;
	t_db	*temp;

	i = 0;
	temp = db;
	while (i < (int)strlen(hash)) {
		temp = temp->next[hash[i] - 48];
		i++;
	}
	return temp->val;
}

int		getPatternDatabase(int *field)
{
	int		i;
	int		h;
	char	*hs;

	i = 1;
	h = 0;
	while (i < 4) {
		if (i == 1) {
			hs = (char *)malloc(sizeof(char) * 17);
			hash(&hs, field, patterns[0]);
			h += find_db(database1, hs);
		} else if (i == 2) {
			hs = (char *)malloc(sizeof(char) * 19);
			hash(&hs, field, patterns[1]);
			h += find_db(database2, hs);
		} else if (i == 3) {
			hs = (char *)malloc(sizeof(char) * 21);
			hash(&hs, field, patterns[2]);
			h += find_db(database3, hs);
		}
		i++;
	}
	return h;
}

int		getTilesOut(int *field)
{
	int		i;
	int		ret;

	ret = 0;
	i = 0;
	while (i < size) {
		if (field[i] != 0) {
			if (i / n - realPos[field[i]].i != 0) {
				ret++;
			}
			if (i % n - realPos[field[i]].j != 0) {
				ret++;
			}
		}
		i++;
	}
	return ret;
}

int		getMisplacedTiles(int *field)
{
	int		i;
	int		ret;

	i = 0;
	ret = 0;
	while (i < size) {
		if (field[i] == 0) {
			if (i != size - 1) {
				ret++;
			}
		} else if (i / n != realPos[field[i]].i || i % n != realPos[field[i]].j) {
			ret++;
		}
		i++;
	}
	return ret;
}

int		getH(int *field)
{
	char	*heu;
	char	*temp;
	int		h;

	temp = strdup(heuristics);
	heu = strtok(temp, "+");
	h = 0;
	while (heu != NULL) {
		if (strcmp(heu, "manhattan") == 0) {
			h += getManhattan(field);
		} else if (strcmp(heu, "linear") == 0) {
			h += getLinearConflict(field);
		} else if (strcmp(heu, "linear2") == 0) {
			h += getLinearConflictMine(field);
		} else if (strcmp(heu, "patternDatabase") == 0) {
			h += getPatternDatabase(field);
		} else if (strcmp(heu, "tilesOut") == 0) {
			h += getTilesOut(field);
		} else if (strcmp(heu, "misplacedTiles") == 0) {
			h += getMisplacedTiles(field);
		} else if (strcmp(heu, "euclideanDistance") == 0) {
			h += getManhattan(field);
		}
		heu = strtok(NULL, "+");
	}
	return h;
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

void	print_field(t_state *node)
{
	int		i;
	int		j;

	i = 0;
	// printf("H = %d\n", node->h);
	while (i < n)
	{
		j = 0;
		while (j < n)
		{
			printf("%d ", node->field[i * n + j]);
			j++;
		}
		i++;
		printf("\n");
	}
	printf("----------------------------------\n");
}

void	print_way(t_state *node)
{
	int		len = 0;

	while (node != NULL)
	{
		// print_field(node);
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
		print_way(node);
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
	// print_field(initial);
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

	if ((*list) == NULL) {
		(*list) = (t_sts *)malloc(sizeof(t_sts));
		(*list)->state = app;
		(*list)->next = NULL;
	} else {
		new = *list;
		while(new->next != NULL) {
			new = new->next;
		}
		new->next = (t_sts *)malloc(sizeof(t_sts));
		new->next->state = app;
		new->next->next = NULL;
	}
}

void	debag(t_sts	*bem)
{
	while(bem != NULL) {
		print_field(bem->state);
		bem = bem->next;
	}
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
	print_field(initial);
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
				succ->g = current->g + 1;
				succ->h = succ->g + getH(succ->field);
				if (not_in(opened, succ)) {
					append(&opened, succ);
				}
			}
			i++;
		}
	}
	free(initial);
}

t_state	*popleft(t_sts **list)
{
	t_state	*ret;
	t_sts	*fr;

	ret = (*list)->state;
	fr = (*list);
	(*list) = (*list)->next;
	free(fr);
	return ret;
}

void	bfs(int *initial_field)
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
	opened = (t_sts *)malloc(sizeof(t_sts));
	closed = (t_sts *)malloc(sizeof(t_sts));
	opened->state = initial;
	closed->state = NULL;
	opened->next = NULL;
	closed->next = NULL;
	// print_field(initial);
	while(opened) {
		current = popleft(&opened);
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
				// if (not_in(opened, succ)) {
				append(&opened, succ);
				// }
			}
			i++;
		}
	}
	free(initial);
}

int		checkHeur(char *check)
{
	char	*heu;
	char	*temp;

	temp = strdup(heuristics);
	heu = strtok(temp, "+");
	while (heu != NULL) {
		if (strcmp(heu, check) == 0) {
			return 1;
		}
		heu = strtok(NULL, "+");
	}
	return 0;
}

int     index_of(int val, int *arr, int size)
{
    int     i;

    i = 0;
    while (i < size)
    {
        if ()
    }
}

float	python(int sz, char *field, char *algo, char *heurs)
{
	int				*initial_field;
	int				i;
	int				j;
	struct timeval	stop, start;
	int             *snake_field;

	n = sz;
	size = n * n;
	initial_field = (int *)malloc(sizeof(int) * size);
	i = 0;
	j = 0;
	snake_field = get_snake(n);
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
	heuristics = heurs;
	if (checkHeur("patternDatabase")) {
		readDatabases();
	}
	gettimeofday(&start, NULL);
	if (strcmp("idaStar", algo) == 0) {
		idaStar(initial_field);
	} else if (strcmp("aStar", algo) == 0) {
		aStar(initial_field);
	} else if (strcmp("bfs", algo) == 0) {
		bfs(initial_field);
	}
	gettimeofday(&stop, NULL);
	// printf("took %f\n", (stop.tv_sec - start.tv_sec) * 1000.0f + (stop.tv_usec - start.tv_usec) / 1000.0f);
	free(left_range);
	free(right_range);
	free(top_range);
	free(bottom_range);
	return (stop.tv_sec - start.tv_sec) * 1000.0f + (stop.tv_usec - start.tv_usec) / 1000.0f;
}
