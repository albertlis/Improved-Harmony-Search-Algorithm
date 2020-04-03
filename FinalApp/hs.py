import numpy as np


class HS:
    def __init__(self, parameters):
        self.fun = parameters[0]
        self.iterations = parameters[1]
        self.hms, self.hmcr = parameters[2:4]
        self.parMin, self.parMax = parameters[4:6]
        self.bandwidthMin, self.bandwidthMax = parameters[-2:]
        numberOfVariables = 5       #zaimplementować z parsera
        self.hm = np.random.uniform(-self.bandwidthMax, self.bandwidthMax, [self.hms, numberOfVariables])

    def __str__(self):
        return "function: '%s' iterations: %d HMS: %d HMCR: %f PARmin: %f PARmax: %f bandwidthMin: %f bandwidthMax: %f" \
               "\n\n " \
               "%s" \
              % (self.fun, self.iterations, self.hms, self.hmcr, self.parMin, self.parMax, self.bandwidthMin,
                 self.bandwidthMax, self.hm)


if __name__ == "__main__":
    hs = HS(("abc", 1, 5, .5, 0.2, 0.8, 10.0, 20.0))
    print(hs)

