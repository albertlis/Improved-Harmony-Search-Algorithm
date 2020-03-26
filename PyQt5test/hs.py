import numpy as np


class HS:
    def __init__(self, parameters):
        self.fun = parameters[0]
        self.iterations = parameters[1]
        self.hms, self.hmcr, self.par, self.b = parameters[-4:]
        numberOfVariables = 5       #zaimplementować z parsera
        self.HM = np.random.uniform(-self.b, self.b, [self.hms, numberOfVariables])


if __name__ == "__main__":
    hs = HS(('x^2', 1, 5, 0.0, 0.0, 10.0))
    print(hs.HM)
    print()
    print("function: '%s' iterations: %d HMS: %d HMCR: %f PAR: %f b: %f" % (hs.fun, hs.iterations, hs.hms, hs.hmcr, hs.par, hs.b))
