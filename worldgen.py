from perlin import PerlinNoiseFactory  # загрузка генератора шума Перлина.
import PIL.Image
import time
import os


class world:  # создавае-мый из main.py класс мира, содержащий в себе все сведения об объекте игрового мира
    def __init__(self, size, tile, octaves,
                 seed):  # генерация мира по введенным параметрам. Параметры следует перенести куда-то, потому что после генерации мира они уже частично неинтересны

        self.size = int(size)  # размер карты
        self.res = int(tile)  # размер тайлов
        self.frames = 40
        self.frameres = 40
        self.space_range = self.size // self.res  # количество тайлов
        self.frame_range = self.frames // self.frameres
        self.seed = seed  # семя генератора
        self.save_path = None  # файл карты
        self.octaves = int(octaves)  # количества октав генератора

        t1 = time.time()
        self.pnf = PerlinNoiseFactory(3, self.seed, octaves=self.octaves, tile=(
            self.space_range, self.space_range, self.frame_range))  # объект трехмерного шума перлина
        print('DEBUG : Perlin noise has been generated.')
        t2 = time.time() - t1
        print('DEBUG : Perlin noise has been generated for %d seconds.)' % (t2))

        self.map_tiles = []  # карта

        self.img = self.draw_image()
        self.log = open('log.txt', 'a')
        # heights_analysis(self.map_tiles)
        self.save_path = '/map/%dkm_world_tile%d_%s.png' % (self.frames, self.space_range, self.seed)
        self.img.save(os.getcwd().replace('\\', '/') + self.save_path)
        timestamp = time.ctime(time.time())
        self.log.write("World generation start has been done at: %s" % (timestamp) + '\n')
        self.log.close()
        return None

    def heights_analysis(self, map_tiles):  # объект, записывающий в лог сведения о мире (высоты и таймштампы)
        heigh = []  # создание
        for x in range(len(map_tiles)):
            new_heigh = map_tiles[x][2]
            heigh.append(new_heigh)
        heigh.sort()
        print(len(heigh))
        min_heigh = heigh[0]
        max_heigh = heigh[len(heigh) - 1]
        print('Min heigh is', min_heigh)
        print('Max heigh is', max_heigh)
        self.log.write("World max heigh point: %d" % (min_heigh) + '\n')
        self.log.write("World min heigh point: %d" % (max_heigh) + '\n')
        amount = 0
        for x in range(len(heigh)):
            amount = amount + heigh[x]
            average = amount / len(heigh)

        # for x in range(map_tiles):
        # for y in range(map_tiles):
        # print(map_tiles[x][y])

        print(amount)
        print(average)
        self.log.write("World average heigh point: %d" % (average) + '\n')

        return None

    def draw_image(self):
        for t in range(1):
            t1 = time.time()
            print('DEBUG : Start drawing image.')
            img = PIL.Image.new('RGB', (self.size, self.size))
            for x in range(self.size):
                for y in range(self.size):
                    n = self.pnf(x / self.res, y / self.res, t / self.frameres)
                    z = (int((n + 1) / 2 * 255 + 0.5))  # получение высоты тайла
                    if z < 90:  # 95 уровень воды
                        img.putpixel((x, y), (0, 0, z))
                    elif z > 150:  # уровень гор
                        if z > 165:
                            cliff = z - 30
                            img.putpixel((x, y), (cliff, cliff, cliff))
                        else:
                            img.putpixel((x, y), (z, z, z))
                    else:
                        img.putpixel((x, y), (0, z, 0))

        t2 = time.time() - t1
        print('DEBUG : Image has been drawed for %d seconds.)' % (t2))
        return img


class Region(world):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.biom = None
        if z < 100:  # определение уровня воды
            self.biom = 'Water'
        elif z > 150:  # уровень гор
            if z > 165:  # уровень высокогорья
                self.biom = 'Highlands'
            else:
                self.biom = 'Mountians'
        else:
            self.biom = 'Forest'  # генератор региона 100х100


class ZArray:
    __slots__ = ["_array"]

    def __init__(self, ini_state):
        self._array = [None for i in range(ini_state)]

    def __getitem__(self, idx):
        return self._array[idx]

    def __setitem__(self, idx, value):
        if idx < 0:
            raise Exception("Out of bounds")
        for i in range((idx + 1) - len(self._array)):
            self._array.append(None)
        self._array[idx] = value

    def __str__(self):
        return "ZArray(" + ", ".join(list(map(str, self._array))) + ")"


class Map:
    def __init__(self, x_size, y_size, ini_state=256):
        self.x_size = x_size
        self.y_size = y_size
        self._map = [[ZArray(ini_state) for i in range(x_size)] for i in range(y_size)]

    def __getitem__(self, tup):
        y, x, z = tup
        if (self.y_size > y and y >= 0) and (self.x_size > x and x >= 0):
            return self._map[y][x][z]
        raise Exception("Out of bounds")

    def __setitem__(self, tup, value):
        y, x, z = tup
        if (self.y_size > y and y >= 0) and (self.x_size > x and x >= 0):
            self._map[y][x][z] = value
            return
        raise Exception("Out of bounds")  # карта, хранящая x,y,z координаты и привязанный объект (region)
