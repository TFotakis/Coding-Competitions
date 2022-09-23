import sys


class Grid(object):
    def __init__(self, rows, columns, minIngredients, maxIngredients, ingredients):
        self.rows = rows
        self.columns = columns
        self.grid = ingredients
        self.minIngredients = minIngredients
        self.maxIngredients = maxIngredients
        self.slices = []

    def __str__(self):
        return ('%dx%d, %d minIngredients, %d maxIngredients\nPizza:\n%s' % (
            self.rows, self.columns, self.minIngredients, self.maxIngredients,
            '\n'.join([''.join([str(self.grid[i][j]) for j in range(self.columns)]) for i in range(self.rows)])))

        # def get_nearest_warehouse_with_product(self, r, c, product_type, num_items, order):
        # min_dist = 999999999
        # warehouse = None
        # for i in range(0, len(self.warehouses)):
        # if self.warehouses[i].products[product_type] > 0:
        # distance1 = get_distance(r, c,
        #                          self.warehouses[i].r,
        #                          self.warehouses[i].c)
        # distance2 = get_distance(self.warehouses[i].r,
        #                          self.warehouses[i].c,
        #                          order.r,
        #                          order.c)
        # distance = distance1 + distance2
        # if distance < min_dist:
        #     warehouse = self.warehouses[i]
        # min_dist = distance
        # return warehouse


        # def product_type_available(self, product_type):
        # for warehouse in self.warehouses:
        #     if warehouse.products[product_type] > 0:
        #         return True
        # return False


class Slice(object):
    def __init__(self, r1, c1, r2, c2):
        self.r1 = r1
        self.c1 = c1
        self.r2 = r2
        self.c2 = c2

    def __str__(self):
        return '%d %d %d %d\n' % (self.r1, self.c1, self.r2, self.c2)


def read_file(filename):
    grid = None
    # ingredients = []
    with open(filename, 'r') as fin:
        line = fin.readline()
        rows, columns, minIngredients, maxIngredients = [int(num) for num in line.split()]
        ingredients = [[0 for x in range(columns)] for y in range(rows)]
        for i in range(rows):
            ingredients[i] = list(fin.readline().strip())
        grid = Grid(rows, columns, minIngredients, maxIngredients, ingredients)
    return grid


def calculate_area(slice):
    return abs(slice.r1 - slice.r2) * abs(slice.c1 - slice.c2)


def cut(grid):

    return 0


def write_file(grid, filename):
    with open(filename, 'w') as fout:
        fout.write('%d\n' % len(grid.slices))
        for slice in grid.slices:
            fout.write(str(slice))


def main():
    if len(sys.argv) < 3:
        sys.exit('Syntax: %s <filename> <output>' % sys.argv[0])
    print('Running on file: %s' % sys.argv[1])
    grid = read_file(sys.argv[1])
    print(grid)
    # slices = []
    try:
        cut(grid)
        # slices.append(Slice(0,1,2,3))
        # slices.append(Slice(4,5,6,7))
        # grid.slices = slices
    except KeyboardInterrupt:
        pass
    write_file(grid, sys.argv[2])
    print('Total Slices:%d' % len(grid.slices))
    sum = 0
    for slice in grid.slices:
        sum += calculate_area(slice)
    print('Total cells used:%d' % sum)


if __name__ == '__main__':
    main()
