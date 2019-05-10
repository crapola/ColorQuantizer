def load_jasc_pal(path):
	with open(path, "r") as file:
		header = next(file)
		version = next(file)
		count = int(next(file))
		lines = file.readlines()  # [3:]
		result = [tuple(map(int, x.rstrip("\n").split(" "))) for x in lines]
		return result